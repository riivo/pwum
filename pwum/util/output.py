class Ouput:
    """For writing html out, simple templating"""
    def __init__(self):

        self.content = ""
        
    def to_file(self, file_name):
        out_file = open(file_name, "w+")
        out_file.write(self.__header.__doc__)
        out_file.write(self.content)
        out_file.write(self.__footer.__doc__)
        out_file.close()
        
    def p(self, title):
        self.content += "{0}<br/>".format(title)
                 
    def h1(self, title):
        self.content += "<h1>{0}</h1>".format(title)
        
    def hr(self):
        self.content += "<hr />"
        
    def table(self):
        self.content += "<table border='1'>"
        
    def end_table(self):
        self.content += "</table>"
        

    def tr(self, cells):
        self.content += "<tr>"
        for c in cells:
            self.content += "<td>{0}</td>".format(c)
        self.content += "</tr>"
    
    def __footer(self):
        """
        </body>
        </html>
        """
    def __header(self):
        """
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> 
        
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
        
        <head>
        <title>Clickstream info</title>
        <style>
        body {
          background:white; color:#222;
          font:13px georgia, serif;
          line-height:1.4;
          font-weight: lighter;
        }
        </style>
        
        </head>
        """