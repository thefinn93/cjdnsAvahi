'''
Created on 20/01/2011

v0.1 (C) Gerald Storer
MIT License

Based on JSON.minify.js: 
https://github.com/getify/JSON.minify
'''

import re

def json_minify(json,strip_space=True):
    tokenizer=re.compile('"|(/\*)|(\*/)|(//)|\n|\r')
    in_string = False
    in_multiline_comment = False
    in_singleline_comment = False
    
    new_str = []
    from_index = 0 # from is a keyword in Python
    
    for match in re.finditer(tokenizer,json):
        
        if not in_multiline_comment and not in_singleline_comment:
            tmp2 = json[from_index:match.start()]
            if not in_string and strip_space:
                tmp2 = re.sub('[ \t\n\r]*','',tmp2) # replace only white space defined in standard
            new_str.append(tmp2)
            
        from_index = match.end()
        
        if match.group() == '"' and not in_multiline_comment and not in_singleline_comment:
            escaped = re.search('(\\\\)*$',json[:match.start()])
            if not in_string or escaped is None or len(escaped.group()) % 2 == 0:
                # start of string with ", or unescaped " character found to end string
                in_string = not in_string
            from_index -= 1 # include " character in next catch
            
        elif match.group() == '/*' and not in_string and not in_multiline_comment and not in_singleline_comment:
            in_multiline_comment = True
        elif match.group() == '*/' and not in_string and in_multiline_comment and not in_singleline_comment:
            in_multiline_comment = False
        elif match.group() == '//' and not in_string and not in_multiline_comment and not in_singleline_comment:
            in_singleline_comment = True
        elif (match.group() == '\n' or match.group() == '\r') and not in_string and not in_multiline_comment and in_singleline_comment:
            in_singleline_comment = False
        elif not in_multiline_comment and not in_singleline_comment and (  
             match.group() not in ['\n','\r',' ','\t'] or not strip_space):
                new_str.append(match.group()) 
    
    new_str.append(json[from_index:])
    return ''.join(new_str)
