from django_assets import Bundle, register

#Javascript
register('all_js',
        Bundle(
               'js/jquery.foundation.accordion.js',
               'js/jquery.foundation.alerts.js',
               'js/jquery.foundation.buttons.js',
               'js/jquery.foundation.clearing.js',
               'js/jquery.foundation.forms.js',
               'js/jquery.foundation.joyride.js',
               'js/jquery.foundation.magellan.js',
               'js/jquery.foundation.mediaQueryToggle.js',
               'js/jquery.foundation.navigation.js',
               'js/jquery.foundation.orbit.js',
               'js/jquery.foundation.reveal.js',
               'js/jquery.foundation.tabs.js',
               'js/jquery.foundation.tooltips.js',
               'js/jquery.foundation.topbar.js',
               'js/jquery-ajax-validation.js',
               'js/app.js',
        ),
        filters='jsmin',
        output='cache/packed.js')

#Css
register('all_css',
        Bundle(
               'css/foundation.css',
               'css/accessibility_foundicons.css',
               'css/general_foundicons.css',
               'css/app.css',
        ),
        filters='cssmin',
        output='cache/packed.css')
