
SECRET_KEY = 'fake_secret_key_for_sphinx_docs_generation'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'bootstrap4',
    'markdown',
    'djangocodemirror'
]

# Code Mirror
CODEMIRROR_THEMES = {
    'darcula': 'CodeMirror/theme/darcula.css',
    'idea': 'CodeMirror/theme/idea.css'
}

CODEMIRROR_MODES = {
    "apl": "CodeMirror/mode/apl/apl.js",
    "asterisk": "CodeMirror/mode/asterisk/asterisk.js",
    "clike": "CodeMirror/mode/clike/clike.js",
    "clojure": "CodeMirror/mode/clojure/clojure.js",
    "cobol": "CodeMirror/mode/cobol/cobol.js",
    "coffeescript": "CodeMirror/mode/coffeescript/coffeescript.js",
    "commonlisp": "CodeMirror/mode/commonlisp/commonlisp.js",
    "css": "CodeMirror/mode/css/css.js",
    "cypher": "CodeMirror/mode/cypher/cypher.js",
    "d": "CodeMirror/mode/d/d.js",
    "diff": "CodeMirror/mode/diff/diff.js",
    "django": "CodeMirror/mode/django/django.js",
    "eiffel": "CodeMirror/mode/eiffel/eiffel.js",
    "erlang": "CodeMirror/mode/erlang/erlang.js",
    "fortran": "CodeMirror/mode/fortran/fortran.js",
    "gas": "CodeMirror/mode/gas/gas.js",
    "gherkin": "CodeMirror/mode/gherkin/gherkin.js",
    "go": "CodeMirror/mode/go/go.js",
    "groovy": "CodeMirror/mode/groovy/groovy.js",
    "haml": "CodeMirror/mode/haml/haml.js",
    "haskell": "CodeMirror/mode/haskell/haskell.js",
    "haxe": "CodeMirror/mode/haxe/haxe.js",
    "htmlmixed": "CodeMirror/mode/htmlmixed/htmlmixed.js",
    "http": "CodeMirror/mode/http/http.js",
    "javascript": "CodeMirror/mode/javascript/javascript.js",
    "livescript": "CodeMirror/mode/livescript/livescript.js",
    "lua": "CodeMirror/mode/lua/lua.js",
    "markdown": "CodeMirror/mode/markdown/markdown.js",
    "mirc": "CodeMirror/mode/mirc/mirc.js",
    "nginx": "CodeMirror/mode/nginx/nginx.js",
    "octave": "CodeMirror/mode/octave/octave.js",
    "pascal": "CodeMirror/mode/pascal/pascal.js",
    "perl": "CodeMirror/mode/perl/perl.js",
    "xml": "CodeMirror/mode/xml/xml.js",
    "php": "CodeMirror/mode/php/php.js",
    "python": "CodeMirror/mode/python/python.js",
    "properties": "CodeMirror/mode/properties/properties.js",
    "q": "CodeMirror/mode/q/q.js",
    "r": "CodeMirror/mode/r/r.js",
    "rpm": "CodeMirror/mode/rpm/rpm.js",
    "rst": "CodeMirror/mode/rst/rst.js",
    "ruby": "CodeMirror/mode/ruby/ruby.js",
    "rust": "CodeMirror/mode/rust/rust.js",
    "sass": "CodeMirror/mode/sass/sass.js",
    "scheme": "CodeMirror/mode/scheme/scheme.js",
    "shell": "CodeMirror/mode/shell/shell.js",
    "smalltalk": "CodeMirror/mode/smalltalk/smalltalk.js",
    "sql": "CodeMirror/mode/sql/sql.js",
    "stex": "CodeMirror/mode/stex/stex.js",
    "vb": "CodeMirror/mode/vb/vb.js",
    "vbscript": "CodeMirror/mode/vbscript/vbscript.js",
    "xquery": "CodeMirror/mode/xquery/xquery.js",
    "yaml": "CodeMirror/mode/yaml/yaml.js",
}

CODEMIRROR_SETTINGS = {
    'darcula': {
        'lineNumbers': True,
        'smartIndent': False,
        'themes': ['darcula'],
        'theme': 'darcula',
        'tabSize': 4,
        'mode': 'text/x-c++src',
        'modes': ["shell", "clike", "htmlmixed", "javascript", "xml", "perl", "python", "ruby"],
        'matchBrackets': True,
        'continueComments': "Enter",
        'addons': [
            "CodeMirror/addon/edit/matchbrackets.js",
            "CodeMirror/addon/comment/continuecomment.js",
            "CodeMirror/addon/comment/comment.js",
            "CodeMirror/addon/display/fullscreen.js"
        ],
        'extra_css': [
            "CodeMirror/addon/display/fullscreen.css"
        ],
    },
    'idea': {
        'lineNumbers': True,
        'smartIndent': False,
        'themes': ['idea'],
        'theme': 'idea',
        'tabSize': 4,
        'mode': 'text/x-c++src',
        'modes': ["shell", "clike", "htmlmixed", "javascript", "xml", "perl", "python", "ruby"],
        'matchBrackets': True,
        'continueComments': "Enter",
        'addons': [
            "CodeMirror/addon/edit/matchbrackets.js",
            "CodeMirror/addon/comment/continuecomment.js",
            "CodeMirror/addon/comment/comment.js",
            "CodeMirror/addon/display/fullscreen.js"
        ],
        'extra_css': [
            "CodeMirror/addon/display/fullscreen.css"
        ],
    },
    'markdown_darcula': {
        'smartIndent': False,
        'lineWrapping': True,
        'themes': ['darcula'],
        'theme': 'darcula',
        'tabSize': 4,
        'mode': 'text/x-markdown',
        'modes': ["markdown"],
        'matchBrackets': True,
        'continueComments': "Enter",
        'addons': [
            "CodeMirror/addon/comment/continuecomment.js",
            "CodeMirror/addon/comment/comment.js",
            "CodeMirror/addon/display/fullscreen.js"
        ],
        'extra_css': [
            "CodeMirror/addon/display/fullscreen.css"
        ],
    },
    'markdown_idea': {
        'smartIndent': False,
        'lineWrapping': True,
        'themes': ['idea'],
        'theme': 'idea',
        'tabSize': 4,
        'mode': 'text/x-markdown',
        'modes': ["markdown"],
        'matchBrackets': True,
        'continueComments': "Enter",
        'addons': [
            "CodeMirror/addon/comment/continuecomment.js",
            "CodeMirror/addon/comment/comment.js",
            "CodeMirror/addon/display/fullscreen.js"
        ],
        'extra_css': [
            "CodeMirror/addon/display/fullscreen.css"
        ],
    },
    'sharecode_darcula': {
        'lineNumbers': True,
        'smartIndent': False,
        'themes': ['darcula'],
        'theme': 'darcula',
        'tabSize': 4,
        'mode': 'text/x-c++src',
        'modes': [
            "apl", "asterisk", "clike", "clojure", "cobol", "coffeescript", "commonlisp", "css", "cypher", "d", "diff",
            "django", "eiffel", "erlang", "fortran", "gas", "gherkin", "go", "groovy", "haml", "haskell", "haxe",
            "htmlmixed", "http", "javascript", "livescript", "lua", "markdown", "mirc", "nginx", "octave", "pascal",
            "perl", "xml", "php", "python", "properties", "q", "r", "rpm", "rst", "ruby", "sass", "scheme",
            "shell", "smalltalk", "sql", "stex", "vb", "vbscript", "xquery", "yaml"
        ],
        'matchBrackets': True,
        'continueComments': "Enter",
        'addons': [
            "CodeMirror/addon/edit/matchbrackets.js",
            "CodeMirror/addon/comment/continuecomment.js",
            "CodeMirror/addon/comment/comment.js",
            "CodeMirror/addon/display/fullscreen.js",
            "CodeMirror/addon/mode/overlay.js",
            "CodeMirror/addon/display/fullscreen.js"
        ],
        'extra_css': [
            "CodeMirror/addon/display/fullscreen.css"
        ],
    },
    'sharecode_idea': {
        'lineNumbers': True,
        'smartIndent': False,
        'themes': ['idea'],
        'theme': 'idea',
        'tabSize': 4,
        'mode': 'text/x-c++src',
        'modes': [
            "apl", "asterisk", "clike", "clojure", "cobol", "coffeescript", "commonlisp", "css", "cypher", "d", "diff",
            "django", "eiffel", "erlang", "fortran", "gas", "gherkin", "go", "groovy", "haml", "haskell", "haxe",
            "htmlmixed", "http", "javascript", "livescript", "lua", "markdown", "mirc", "nginx", "octave", "pascal",
            "perl", "xml", "php", "python", "properties", "q", "r", "rpm", "rst", "ruby", "sass", "scheme",
            "shell", "smalltalk", "sql", "stex", "vb", "vbscript", "xquery", "yaml"
        ],
        'matchBrackets': True,
        'continueComments': "Enter",
        'addons': [
            "CodeMirror/addon/edit/matchbrackets.js",
            "CodeMirror/addon/comment/continuecomment.js",
            "CodeMirror/addon/comment/comment.js",
            "CodeMirror/addon/display/fullscreen.js",
            "CodeMirror/addon/mode/overlay.js",
            "CodeMirror/addon/display/fullscreen.js"
        ],
        'extra_css': [
            "CodeMirror/addon/display/fullscreen.css"
        ],
    },
}
