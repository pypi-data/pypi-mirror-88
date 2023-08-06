"""Support for Zope interfaces."""

import ast
import re

import astor
from pydoctor import astbuilder, model


class ZopeInterfaceModule(model.Module):
    def setup(self):
        super().setup()
        self.implements_directly = [] # [name of interface]

    @property
    def allImplementedInterfaces(self):
        """Return all the interfaces provided by this module
        """
        return list(self.implements_directly)


class ZopeInterfaceClass(model.Class):
    isinterface = False
    isschemafield = False
    isinterfaceclass = False
    implementsOnly = False
    implementedby_directly = None # [objects], when isinterface == True
    def setup(self):
        super().setup()
        self.implements_directly = [] # [name of interface]

    @property
    def allImplementedInterfaces(self):
        """Return all the interfaces implemented by this class.

        This returns them in something like the classic class MRO.
        """
        r = list(self.implements_directly)
        if self.implementsOnly:
            return r
        for b in self.baseobjects:
            if b is None:
                continue
            for interface in b.allImplementedInterfaces:
                if interface not in r:
                    r.append(interface)
        return r

    @property
    def allImplementations(self):
        r = list(self.implementedby_directly)
        stack = list(r)
        while stack:
            c = stack.pop(0)
            for sc in c.subclasses:
                if sc.implementsOnly:
                    continue
                stack.append(sc)
                if sc not in r:
                    r.append(sc)
        return r


def _inheritedDocsources(obj):
    if not isinstance(obj.parent, (model.Class, model.Module)):
        return
    name = obj.name
    for interface in obj.parent.allImplementedInterfaces:
        io = obj.system.objForFullName(interface)
        if io is not None:
            for io2 in io.allbases(include_self=True):
                if name in io2.contents:
                    yield io2.contents[name]

class ZopeInterfaceFunction(model.Function):
    def docsources(self):
        yield from super().docsources()
        yield from _inheritedDocsources(self)

class ZopeInterfaceAttribute(model.Attribute):
    def docsources(self):
        yield from super().docsources()
        yield from _inheritedDocsources(self)

def addInterfaceInfoToScope(scope, interfaceargs):
    for arg in interfaceargs:
        # If you do implementer(*()), the argument ends up being None, which we
        # should skip
        if arg is None:
            continue

        if not isinstance(arg, tuple):
            fullName = scope.expandName(astor.to_source(arg).strip())
        else:
            fullName = arg[1]
        obj = scope.system.objForFullName(fullName)
        if isinstance(obj, ZopeInterfaceClass):
            scope.implements_directly.append(fullName)
            if not obj.isinterface:
                scope.report(
                    'probable interface %s not marked as such' % fullName,
                    section='zopeinterface')
                obj.isinterface = True
                obj.kind = "Interface"
                obj.implementedby_directly = []
            obj.implementedby_directly.append(scope)
        elif obj is not None:
            scope.report(
                'probable interface %s not detected as a class' % fullName,
                section='zopeinterface')

def addInterfaceInfoToModule(module, interfaceargs):
    addInterfaceInfoToScope(module, interfaceargs)

def addInterfaceInfoToClass(cls, interfaceargs, implementsOnly):
    cls.implementsOnly = implementsOnly
    if implementsOnly:
        cls.implements_directly = []
    addInterfaceInfoToScope(cls, interfaceargs)


schema_prog = re.compile(r'zope\.schema\.([a-zA-Z_][a-zA-Z0-9_]*)')
interface_prog = re.compile(
    r'zope\.schema\.interfaces\.([a-zA-Z_][a-zA-Z0-9_]*)'
    r'|zope\.interface\.Interface')

def namesInterface(system, name):
    if interface_prog.match(name):
        return True
    obj = system.objForFullName(name)
    if not obj or not isinstance(obj, model.Class):
        return False
    return obj.isinterface

class ZopeInterfaceModuleVisitor(astbuilder.ModuleVistor):

    def funcNameFromCall(self, node):
        if isinstance(node.func, ast.Name):
            name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            name = astor.to_source(node).strip().split("(")[0]
        elif isinstance(node.func, ast.Call):
            return self.funcNameFromCall(node.func)
        else:
            return None
        return self.builder.current.expandName(name)

    def _handleAssignmentInModule(self, target, annotation, expr, lineno):
        super()._handleAssignmentInModule(
                target, annotation, expr, lineno)

        if not isinstance(expr, ast.Call):
            return
        funcName = self.funcNameFromCall(expr)
        if funcName is None:
            return
        ob = self.system.objForFullName(funcName)
        if isinstance(ob, model.Class) and ob.isinterfaceclass:
            # TODO: Process 'bases' and '__doc__' arguments.
            interface = self.builder.pushClass(target, lineno)
            interface.isinterface = True
            interface.implementedby_directly = []
            interface.bases = []
            interface.baseobjects = []
            self.builder.popClass()
            self.newAttr = interface

    def _handleAssignmentInClass(self, target, annotation, expr, lineno):
        super()._handleAssignmentInClass(
                target, annotation, expr, lineno)

        def handleSchemaField():
            keywords = {arg.arg: arg.value for arg in expr.keywords}
            descrNode = keywords.get('description')
            if isinstance(descrNode, ast.Str):
                attr.setDocstring(descrNode)
            elif descrNode is not None:
                attr.report(
                    'description of field "%s" is not a string literal'
                    % attr.name, section='zopeinterface')

        if not isinstance(expr, ast.Call):
            return
        attr = self.builder.current.contents.get(target)
        if attr is None:
            return
        funcName = self.funcNameFromCall(expr)
        if funcName is None:
            return
        if funcName == 'zope.interface.Attribute':
            attr.kind = 'Attribute'
            args = expr.args
            if len(args) == 1 and isinstance(args[0], ast.Str):
                attr.setDocstring(args[0])
            else:
                attr.report(
                    'definition of attribute "%s" should have docstring '
                    'as its sole argument' % attr.name,
                    section='zopeinterface')
        elif schema_prog.match(funcName):
            attr.kind = schema_prog.match(funcName).group(1)
            handleSchemaField()
        else:
            cls = self.builder.system.objForFullName(funcName)
            if isinstance(cls, ZopeInterfaceClass) and cls.isschemafield:
                attr.kind = cls.name
                handleSchemaField()

    def visit_Call(self, node):
        base = self.funcNameFromCall(node)
        if base is None:
            return
        meth = getattr(self, "visit_Call_" + base.replace('.', '_'), None)
        if meth is not None:
            meth(base, node)

    def visit_Call_zope_interface_moduleProvides(self, funcName, node):
        if not isinstance(self.builder.current, model.Module):
            self.default(node)
            return

        addInterfaceInfoToModule(self.builder.current, node.args)

    def visit_Call_zope_interface_implements(self, funcName, node):
        if not isinstance(self.builder.current, model.Class):
            self.default(node)
            return
        addInterfaceInfoToClass(self.builder.current, node.args,
                                funcName == 'zope.interface.implementsOnly')
    visit_Call_zope_interface_implementsOnly = visit_Call_zope_interface_implements

    def visit_Call_zope_interface_classImplements(self, funcName, node):
        clsname = self.builder.current.expandName(
            astor.to_source(node.args[0]).strip())
        if clsname not in self.system.allobjects:
            self.builder.system.msg(
                "parsing",
                "classImplements on unknown class %r"%clsname)
            return
        cls = self.system.allobjects[clsname]
        addInterfaceInfoToClass(cls, node.args[1:],
                                funcName == 'zope.interface.classImplementsOnly')
    visit_Call_zope_interface_classImplementsOnly = visit_Call_zope_interface_classImplements

    def visit_ClassDef(self, node):
        super().visit_ClassDef(node)
        cls = self.builder.current.contents.get(node.name)
        if cls is None:
            return

        bases = []

        for base in cls.bases:
            if isinstance(base, ast.Name):
                bases.append(self.builder.current.expandName(base.id))
            elif isinstance(base, str):
                bases.append(self.builder.current.expandName(base))
            else:
                raise Exception(base)

        if 'zope.interface.interface.InterfaceClass' in bases:
            cls.isinterfaceclass = True

        if any(namesInterface(self.system, b) for b in cls.bases):
            cls.isinterface = True
            cls.kind = "Interface"
            cls.implementedby_directly = []

        for n, o in zip(cls.bases, cls.baseobjects):
            if schema_prog.match(n) or (o and o.isschemafield):
                cls.isschemafield = True

        for ((dn, fn, o), args) in cls.decorators:
            if fn == 'zope.interface.implementer':
                addInterfaceInfoToClass(cls, args, False)


class ZopeInterfaceASTBuilder(astbuilder.ASTBuilder):
    ModuleVistor = ZopeInterfaceModuleVisitor


class ZopeInterfaceSystem(model.System):
    Module = ZopeInterfaceModule
    Class = ZopeInterfaceClass
    Function = ZopeInterfaceFunction
    Attribute = ZopeInterfaceAttribute
    defaultBuilder = ZopeInterfaceASTBuilder
