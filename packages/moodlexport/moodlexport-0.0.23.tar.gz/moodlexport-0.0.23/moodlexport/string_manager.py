
from xml.dom.minidom import parseString
from xml.sax.saxutils import unescape
import io
import base64
from bs4 import BeautifulSoup
from TexSoup import TexSoup


####################################
## GLOBAL CONSTANTS 
####################################

# Dirty but needed : all the fields required to create a question
# We also set their default value, and an alias when the fields has a weird/toolong name
DICT_DEFAULT_QUESTION_MOODLE = { 
    # general stuff
    '@type': {'default': "essay", 
              'alias': 'type'
             }, # can be "multichoice" for MCQs
    "name": {'default': "Default question title", 
             'attribute': {'@format': 'txt'}, 
             'alias': 'title'
            },
    "questiontext": {'default': "Default question text", 
                     'attribute': {'@format': 'html'}, 
                     'alias': 'text'
                    },
    "generalfeedback": {'default': "", 'attribute': {'@format': 'html'}},
    "defaultgrade": {'default': 1.0, 
                     'alias': 'grade'
                    },
    "penalty": {'default': 0.0},
    "hidden": {'default': 0},
    "idnumber": {'default': ""},
    # 'essay' specifics
    "responseformat": {'default': "editorfilepicker"}, # by default allow to upload a file as answer. Set "editor" ottherwise
    "responserequired": {'default': 0}, # 0 for no response required, 1 for yes
    "responsefieldlines": {'default': 10},
    "attachments": {'default': -1}, # number of attachments allowed. -1 is infinty
    "attachmentsrequired": {'default': 0}, # 0 for no attachment required, 1 for yes
    "graderinfo": {'default': "", # correction for the grader
                   'attribute': {'@format': 'html'}, 
                   'alias': 'infocorrecteur'
                  }, 
    "responsetemplate": {'default': "", 'attribute': {'@format': 'html'}},
    # 'multichoice' specifics
    "single" : {'default': "true"}, # Says if only a unique answer is possible
    "shuffleanswers" : {'default': "true"}, # Constantly shuffles the possible choices
    "answernumbering" : {'default': "none"}, # Other choices : 'abc', '123', 'iii', and certainly caps
    "correctfeedback": {'default': "Votre réponse est correcte.", 'attribute': {'@format': 'html'}},
    "partiallycorrectfeedback": {'default': "Votre réponse est partiellement correcte.", 'attribute': {'@format': 'html'}},
    "incorrectfeedback": {'default': "Votre réponse est incorrecte.", 'attribute': {'@format': 'html'}},
    "shownumcorrect" : {'default': ""}, # No idea
    "answer" : {'default': "", 'list': []} # We deal with this in the Answer class
}

def dict_default_question_moodle():
    return DICT_DEFAULT_QUESTION_MOODLE


# to deal with mess between Latex, python and xml special characters
# \u and \x not supported but useless for inline latex?
UNESCAPE_LATEX = { 
    '\x07' : '\\a', 
    '\x0c' : '\\f', 
    '\x0b' : '\\v', 
    '\x08' : '\\b', 
    '\n'   : '\\n', 
    '\r'   : '\\r', 
    '\t'   : '\\t' 
} 


####################################
## STRING FUNCTIONS
####################################

def alias(field): # easy access to alias
    if 'alias' in dict_default_question_moodle()[field]:
        return dict_default_question_moodle()[field]['alias']
    else:
        return field

def isfield(string):
    for key in dict_default_question_moodle().keys():
        if string in [key, alias(key)]:
            return True
    return False

def cleanstr(string, raw=False):
    if raw:
        string = string.replace('\t','') # no tabs
        string = string.replace('\n','') # no linebreak BEWARE this might destroy protected string
    else:
        string = string.replace('\t','  ') # double space instead of tabs
    return string

def savestr(string, filename="new.txt", raw=False):
    string = cleanstr(string, raw)
    text_file = io.open(filename, "w", encoding='utf8') # essential for accents and other characters
    text_file.write(string)
    text_file.close()

def latex_protect(string):
    return unescape(string, UNESCAPE_LATEX)
    
def html(string):
    if string is "":
        return string
    else:
        return "<![CDATA[<p>\(\)" + tex_parse_dollar(latex_protect(string)) + "</p>]]>"  # \(\) is a hack to activate latex dans Moodle. Not always needed, not always working. Still a mystery to me.

def set_oparg(variable, default_value): #optional argument manager
    if variable is None:
        return default_value
    else:
        return variable
    
def printmk(*tuple_of_text):
    from IPython.display import display, Markdown
    L = [Markdown(text) for text in tuple_of_text]
    return display(*tuple(L))


def replace_open_close(string, old, newopen, newclose):
    # Given a string containing PAIRS of 'old' chains of characters
    # replace 'old' with opening/closing chains of characters
    oldsize = len(old)
    target_idx = [idx for idx in range(len(string)) if string[idx:idx+oldsize] == old]
    if len(target_idx) % 2 == 0:
        target_open_idx = target_idx[0::2]
        target_close_idx = target_idx[1::2]
        diff = 0 # controls the difference in size bewtween old and new strings
        gap_open = len(newopen) - oldsize
        for idx in target_open_idx:
            string = string[:idx+diff] + newopen + string[idx+oldsize+diff:]
            diff = gap_open + diff
        diff = gap_open # we reset but not to zero since there is an already replaced "open" character before the first "close" one
        gap_close = len(newclose) - oldsize + gap_open # every time we move forward we accumulate a shit from both "open" and "close" characters
        for idx in target_close_idx:
            string = string[:idx+diff] + newclose + string[idx+oldsize+diff:]
            diff = gap_close + diff
    else:
        raise ValueError("I have to replace '"+old+"' with *pairs* of characters but I see "+str(len(target_idx))+" of them which is an odd number")
    return string

def tex_parse_dollar(latex):
    # Transform a string containing latex expressions to make it compatible with most
    # web-based applications which prefer \(...\) or \[...\] syntax.
    latex = replace_open_close(latex, '$$', '\\[', '\\]')
    latex = replace_open_close(latex, '$', '\\(', '\\)')
    return latex


"""
This was INDECENTLY SLOW. Like 1 full second to convert an empty string?????
I couldn't make any parser to work properly. In the end I hard coded it myself.
It is quite fast now (10000 calls/second), and more robust (allows for newlines etc).

# Taken from https://gist.github.com/erezsh/1f834f7d203cb1ac89b5b3aa877fa634

class T(Transformer):
    def mathmode_offset(self, children):
        return '\\[' + ''.join(children[1:-1]) + '\\]'

    def mathmode_inline(self, children):
        return '\\(' + ''.join(children[1:-1]) + '\\)'

    def tex(self, children):
        return ''.join(children)

def tex_parse_dollar(string):
    lark = Lark(r'''
         tex: (mathmode_offset | mathmode_inline | TEXT)+
         mathmode_offset: OFFSETDOLLAR TEXT+ OFFSETDOLLAR | OFFSETOPEN TEXT+ OFFSETCLOSE
         mathmode_inline: INLINEOPEN TEXT+ INLINECLOSE | INLINE TEXT+ INLINE
         INLINE: "$"
         INLINEOPEN: "\\("
         INLINECLOSE: "\\)"
         OFFSETDOLLAR: "$$"
         OFFSETOPEN: "\\["
         OFFSETCLOSE: "\\]"
         TEXT: /[^\]$]+/s
         ''', start='tex', parser='lalr')
    return T().transform(lark.parse(string)) # string.replace('\n', '') destroys the protected \\n, we need to be smarter here
"""


#-----------------------------------------------------
# Images : python --> html
#-----------------------------------------------------

def img_to_html64(path, **options):
    ''' Given an image path, returns an html string containgin the image in base 64
        OPTIONS:
            width : int
            heigth : int
            alt : string (alternative text)
            style : 'inline' or 'centered' (default). The latter adds <br/> around the image.
    '''
    if 'style' not in options.keys():
        options['style'] = 'centered'
        
    with open(path, "rb") as img_file:
        img64 = base64.b64encode(img_file.read()).decode('utf-8')
    imghtml = '<img src="data:image/png;base64, ' + img64 + '" alt="ALT_TEXT" origin="' + path + '"' 
    for key in ['width', 'height', 'alt', 'style']:
        if key in options.keys():
            imghtml = imghtml + ' ' + key + '="' + str(options[key]) + '"'
    imghtml = imghtml + '>'
    
    if  options['style'] == 'inline':
        return imghtml
    elif options['style'] == 'centered':
        return '</p><p style="text-align: center">' + imghtml + '</p><p>'
    
def includegraphics(path, **options):
    return img_to_html64(path, **options)


#-----------------------------------------------------
# Images : python --> latex
#-----------------------------------------------------

def img64_to_latex(string):
    # we assume the input is a string starting with <img... and ending with ....>
    # and that it has an attribute src="path"
    # the function returns a string \includegraphics[options]{path}
    parsed_html = BeautifulSoup(string, features="lxml")
    dico = parsed_html.find('img').attrs # a dict containing all the attributes of this image tag
    latex = '\\includegraphics'
    
    options = ''
    if 'width' in dico.keys():
        options = options + 'width=' + dico['width'] + 'px,'
    if 'heigth' in dico.keys():
        options = options + 'heigth=' + dico['heigth'] + 'px,'
    if len(options) > 0:
        options = '[' + options[:-1] + ']' # we delete the last comma ','
    
    latex = latex + options + '{' + dico['origin'] + '}'
    
    if 'style' in dico.keys() and dico['style'] == 'centered':
        latex = '\n\\begin{center}\n    ' + latex + '\n\\end{center}\n'
    return latex

def findall(pattern, string):
    '''Yields all the positions of the pattern in the string in an iterator'''
    i = string.find(pattern)
    while i != -1:
        yield i
        i = string.find(pattern, i+1)    

def html_to_latex(string):
    # Input : a string containing eventually html tags
    # we pick each of them and convert them into latex instructions
    ''' we should deal here with all the html code : <br> and also the <p>'s '''
    # the breaklines tags
    string = string.replace('<br/>','\n\n')
    
    # the paragraphs tags
    # those are introduced in the function img_to_html64 and we know exactly what they look like
    string = string.replace('</p><p style="text-align: center">', '') 
    string = string.replace('</p><p>', '')
    
    # the image tags
    # those are introduced in the function img_to_html64 and and are a bit more complicated to deal with
    open_img = list(findall('<img', string)) # list of where are the tags
    if len(open_img) == 0:
        print('fail')
        return string
    else:
        close_img = [string.find('>', idx) for idx in open_img] # list of where the tags get closed
        list_img64 = [img64_to_latex(str(tag)) for tag in BeautifulSoup(string, features="lxml").find_all('img')] # list of strings with the tags
        nb_tag = len(list_img64)
        
        latex = string[:open_img[0]]
        for k in range(nb_tag-1): # for every tag we add the latexified tag, and the non-tag text following
            latex = latex + list_img64[k] + string[close_img[k]+1:open_img[k+1]]
        latex = latex + list_img64[nb_tag-1] + string[close_img[nb_tag-1]+1:]
        return latex

#-----------------------------------------------------
# Images : latex --> python
#-----------------------------------------------------
    
def option_string_to_dict(string):
    # Converts a string like 'a=2, b=3' into a dict { a:2, b:3 }
    # taken from https://stackoverflow.com/questions/20263839/python-convert-a-string-to-arguments-list
    string = string.replace(' ','')
    return dict(e.split('=') for e in string.split(','))

def includegraphics_latex_to_html(string, style):
    # input : a string containing only one latex command 'includegraphics'
    # input : style is 'inline' or 'centered' (see img_to_html64)
    # output : an html string containing an image tag
    arguments = list(TexSoup(string).find_all('includegraphics'))[0].args
    # arguments is a list, containing all the arguments, following the following pattern:
    # if there is only the required argument (here the filepath), it has length 1
    # if there is also n optional arguments, it has length 2,
    if len(arguments) == 1:
        path = arguments[0].value
        options = {}
    elif len(arguments) == 2:
        path = arguments[1].value
        options = option_string_to_dict(arguments[0].value)
        # annoying fix to do because latex wants units like '100px' while html just needs '100'
        for key in options.keys():
            options[key] = options[key].replace('px','')
    else:
        raise ValueError('unknown bug here')
    # ok now we have all we need : 
    options = {**options, 'style' : style }
    return img_to_html64(path, **options)

def convert_centered_images_to_html(latex):
    listbegin = list(findall('\\begin{center}', latex))
    listend = list(findall('\\end{center}', latex))
    listend = [idx + 12 for idx in listend] # we have the real end of the block
    nb_images = len(listbegin)
    if nb_images == 0:
        return latex
    
    output = latex[:listbegin[0]]
    for k in range(nb_images-1):
        string_image = latex[listbegin[k]:listend[k]+1]
        output = output + includegraphics_latex_to_html(string_image, style='centered') + latex[listend[k]+1:listbegin[k+1]]
    string_image = latex[listbegin[nb_images-1]:listend[nb_images-1]+1]
    output = output + includegraphics_latex_to_html(string_image, style='centered') + latex[listend[nb_images-1]+1:]  
    return output

def convert_images_to_html(latex):
    latex = convert_centered_images_to_html(latex)
    imgopen = list(findall('\\includegraphics', latex))
    imgclose = [latex.find('}', idx) for idx in imgopen]
    nb_images = len(imgopen)
    if nb_images == 0:
        return latex
    
    output = latex[:imgopen[0]]
    for k in range(nb_images-1):
        string_image = latex[imgopen[k]:imgclose[k]+1]
        output = output + includegraphics_latex_to_html(string_image, style='inline') + latex[imgclose[k]+1:imgopen[k+1]]
    string_image = latex[imgopen[nb_images-1]:imgclose[nb_images-1]+1]
    output = output + includegraphics_latex_to_html(string_image, style='inline') + latex[imgclose[nb_images-1]+1:]  
    return output

def latex_to_html_cleaner(latex):
    latex = convert_images_to_html(latex)
    latex = latex.replace('\t','')
    latex = latex.replace('\n\n','<br/>')
    latex = latex.replace('\n','')
    return latex










