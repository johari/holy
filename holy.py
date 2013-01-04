import os
import ast

class RubyTransformer(ast.NodeTransformer):

  def map_visit(self, list, join="\n", indent=""):
    r = []
    for item in list:
      indd = (isinstance(item, str) and item or self.visit(item))
      indd = "\n".join([indent+x for x in indd.split("\n")])
      r += [indd]
    return join.join(r)

  def visit_Return(self, node):
    return "return %s" % self.visit(node.value)

  def visit_Index(self, node):
    return "%s" % self.visit(node.value)

  def visit_Slice(self, node):
    dots = "..."
    if node.lower != None:
      lower = self.visit(node.lower)
    else:
      lower = "0"
    if node.upper != None:
      upper = self.visit(node.upper)
    else:
        upper = "-1"
        dots = ".."
    return "%s%s%s" % (lower, dots, upper)

  def visit_Subscript(self, node):
    return "%s[%s]" % (self.visit(node.value), self.visit(node.slice))

  def visit_Num(self, node):
    return str(node.n)

  def visit_Add(self, node):
    return "+"

  def visit_Call(self, node):
    func = self.visit(node.func)
    args = self.map_visit(node.args)
    if func == "len":
      return "%s.length" % (args)
    else:
      return "%s(%s)" % (func, args)

  def visit_AugAssign(self, node):
    return self.map_visit([node.target, self.visit(node.op)+"=", node.value], " ")

  def visit_Expr(self, node):
    return self.visit(node.value)

  def visit_If(self, node):
    orelse = self.map_visit(node.orelse, indent="  ")
    if len(orelse) > 0:
      return "if %s then\n%s\nelse\n%s\nend" %\
        (self.visit(node.test), self.map_visit(node.body, "\n", "  "), orelse)
    else:
      return "if %s then\n%s\nend" %\
        (self.visit(node.test), self.map_visit(node.body, "\n", "  "))

  def visit_Str(self, node):
    return "\"%s\"" % node.s

  def visit_Print(self, node):
    return "puts %s" % self.map_visit(node.values, ",")

  def visit_FunctionDef(self, node):
    args = []
    for arg in node.args.args:
      args += [self.visit(arg)]

    body = []
    for expr in node.body:
      body += [self.visit(expr)]

    return "def %s(%s)\n%s\nend" % (node.name, ", ".join(args),\
      self.map_visit(body, "\n", "  "))

  def visit_Name(self, node):
      reserved = {"False": "false", "True": "true", "None": "nil"}
      try:
        return reserved[node.id]
      except KeyError:
        return node.id

  def visit_Pass(self, node):
    return ";"

  def visit_Module(self, node):
    return self.map_visit(node.body)

  def visit_Eq(self, node):
    return "=="

  def visit_Not(self, node):
    return "!"

  def visit_BinOp(self, node):
    return "%s %s %s" % (self.visit(node.left), self.visit(node.op), self.visit(node.right))

  def visit_Div(self, node):
    return "/"

  def visit_Or(self, node):
    return "or"

  def visit_Break(self, node):
    return "break"

  def visit_Assign(self, node):
    return "%s = %s" % (self.map_visit(node.targets, ", "), self.visit(node.value))

  def visit_Attribute(self, node):
    return self.map_visit([node.value, node.attr], ".")

  def visit_While(self, node):
    return "while %s do\n%s\nend" % (self.visit(node.test), self.map_visit(node.body, indent="  "))

  def visit_And(self, node):
    return "&&"

  def visit_Lt(self, node):
    return "<"

  def visit_Compare(self, node):
    z = zip(node.comparators, node.ops)
    def red(x, y):
      a = ast.BinOp(left=x, op=y[1], right=y[0])
      return ast.fix_missing_locations(a)
    st = reduce(red, z, node.left)
    return self.visit(st)

  def visit_UnaryOp(self, node):
    return "(%s(%s))" % (self.visit(node.op), self.visit(node.operand))

  def visit_BoolOp(self, node):
    return self.map_visit(node.values, join=" "+self.visit(node.op)+" ")

  def visit_List(self, node):
    return "[%s]" % self.map_visit(node.elts, join=", ")

  def visit_For(self, node):
    if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name) \
      and node.iter.func.id == "range":
        return "%s.upto(%s) do |%s|\n%s\nend" % ( \
          self.visit(node.iter.args[0]),
          self.visit(node.iter.args[1]),
          self.visit(node.target),
          self.map_visit(node.body, indent="  ")
          )
    else:
      return None

class Holy():

  def __init__(self, py):
    self.py = py
    self.node = ast.parse(self.py)
    if os.environ["debug"]:
      open("tmp/foo_%s_dump" % os.environ["HACK"], "w").write(ast.dump(self.node))

  def toRuby(self):
    res = RubyTransformer().visit(self.node)
    return res
