from django_assets import Bundle, register

#Javascript
register('all_js',
        Bundle(
            'js/foundation/foundation.js',
            'js/foundation/foundation.dropdown.js',
            'js/foundation/foundation.placeholder.js',
            'js/foundation/foundation.forms.js',
            'js/foundation/foundation.alerts.js',
            'js/foundation/foundation.magellan.js',
            'js/foundation/foundation.reveal.js',
            'js/foundation/foundation.tooltips.js',
            'js/foundation/foundation.clearing.js',
            'js/foundation/foundation.cookie.js',
            'js/foundation/foundation.joyride.js',
            'js/foundation/foundation.orbit.js',
            'js/foundation/foundation.section.js',
            'js/foundation/foundation.topbar.js',
            'js/jquery-ajax-validation.js',
            'js/app.js',
        ),
        filters='jsmin',
        output='cache/packed.js')

#Css
register('all_css',
        Bundle(
               'css/normalize.css',
               'css/foundation.css',
               'css/accessibility_foundicons.css',
               'css/general_foundicons.css',
               'css/app.css',
        ),
        filters='cssmin',
        output='cache/packed.css')

#Scss
register('all_scss',
        Bundle(
               'scss/normalize.scss',
               'scss/foundation.scss',
        ),
        filters='pyscss',
        output='cache/_packed.css')
