import jinja2
from jinja2 import FileSystemLoader

e = jinja2.Environment(loader = FileSystemLoader('tpls/java'))

def camel_case(s):
    return ''.join([ word.capitalize() for word in s.split('_')])

def camel_back(s):
    c = camel_case(s)
    return c[0].lower() + c[1:]

def getJavaFieldName( colName ):
    return camel_back(colName[colName.index('_'):])

def getJavaType(field):
    return field.get_java_type()

def create_java_getter(fieldName,fieldType):
  upperFieldName = fieldName[0].upper() + fieldName[1:]
  return """
  public """ + fieldType + """ get""" + upperFieldName + """() {
      return """ + fieldName + """;
  }"""

def create_java_setter(fieldName,fieldType):
  upperFieldName = fieldName[0].upper() + fieldName[1:]
  return """
  public void set""" + upperFieldName + """(""" + fieldType + """ """ + fieldName + """) {
      this."""+fieldName+""" = """ + fieldName + """;
  }"""

def create_class_name ( table ) :
    return camel_case ( table.name )

def create_field_name ( table ) :
    return camel_back ( table.name )

def create_java_type ( table ):
  source = "class " + table.getClassName() + " {\n"
  
  cols = []
  funcs = []

  for f in table.fields:
    cols.append ( "  @Column\n  private " +getJavaType(f) + " " + getJavaFieldName(f.name) + ";" )
    funcs.append ( create_java_getter ( getJavaFieldName(f.name) , getJavaType(f) ) )
    funcs.append ( create_java_setter ( getJavaFieldName(f.name) , getJavaType(f) ) )

  for a in table.associations:
    if a.tableFrom == table: # single item
        cols.append ( "@Column\n  private " + create_class_name(a.tableTo) + " " + create_field_name ( a.tableTo ) + ";" )
        funcs.append ( create_java_getter ( create_field_name ( a.tableTo ) , create_class_name(a.tableTo) ) )
        funcs.append ( create_java_setter ( create_field_name ( a.tableTo ) , create_class_name(a.tableTo) ) )
    elif a.tableTo == table: # collection
        cols.append ( "@Column\n  private List<" + create_class_name(a.tableFrom) + "> " + create_field_name ( a.tableFrom ) + "s;" )

  source += "\n".join(cols)
  source += "\n"
 
  source += "\n".join(funcs)
  
  source += "\n}\n"

  return source

def get_signatures_for_table ( table ):
    signatures = [( table.getClassName(), "insert" + table.getClassName(), table.getClassName() ),
                  ( table.getClassName(), "delete" + table.getClassName(), table.getClassName() ),
                  ( table.getClassName(), "update" + table.getClassName(), table.getClassName() ),
                  ( table.getClassName(), "selectPk" + table.getClassName(), table.getClassName() )]

    return signatures

def create_sproc_service_interface( table ):
    t = e.get_template('sproc_interface.java')

    sproc_list = ""
    l = get_signatures_for_table ( table )
    for (r,n,p) in l:
        sproc_list += "  public " + r + " " + n + "( " + r + " "+r+" );\n"

    return t.render(interfaceName=table.getClassName()+"SProcService",
                    sprocList=sproc_list)

def create_sproc_service_implementation( table ):
    t = e.get_template('sproc_implementation.java')

    sproc_list = ""
    l = get_signatures_for_table ( table )

    for (field_name, method_name, p) in l:
        lower_field_name = field_name[0].lower() + field_name[1:]
        sproc_list += "    public " + field_name + " " + method_name + "(" + field_name + " " + lower_field_name + """) {
        return sproc."""+method_name+"""(""" + lower_field_name + """);
    }\n\n"""

    return t.render( interfaceName=table.getClassName()+"SProcService",
                     functionImplementations=sproc_list,
                     datasourceProvider='DataSourceProvider' )
