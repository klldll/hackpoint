from django_assets import Bundle, register

#Javascript
register('all_js',
        Bundle(
            'js/foundation/foundation.js',
            'js/foundation/foundation.abide.js',
            'js/foundation/foundation.accordion.js',
            'js/foundation/foundation.alert.js',
            'js/foundation/foundation.clearing.js',
            'js/foundation/foundation.dropdown.js',
            'js/foundation/foundation.equalizer.js',
            'js/foundation/foundation.interchange.js',
            'js/foundation/foundation.joyride.js',
            'js/foundation/foundation.magellan.js',
            'js/foundation/foundation.offcanvas.js',
            'js/foundation/foundation.orbit.js',
            'js/foundation/foundation.reveal.js',
            'js/foundation/foundation.slider.js',
            'js/foundation/foundation.tab.js',
            'js/foundation/foundation.tooltip.js',
            'js/foundation/foundation.topbar.js',

            'js/jquery.cookie.js',
            'js/jquery-ajax-validation.js',
            'js/app.js',
        ),
        filters='jsmin',
        output='cache/packed.js')

#Scss
scss = Bundle(
       'scss/normalize.scss',
       #'scss/_settings.scss',
       'scss/app.scss',
       #'scss/foundation.scss',
        filters='scss',
        output='cache/scss.css'
)

#Css
register('all_css',
        Bundle(
               scss,
               'css/accessibility_foundicons.css',
               'css/general_foundicons.css',
               'css/app.css',
        ),
        filters='cssmin',
        output='cache/packed.css')

