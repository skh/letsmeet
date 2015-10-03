/* script.js */
// see https://github.com/zurb/foundation/issues/5551
// workaround to make topbar dropdowns close on second click
$( 'nav.top-bar:not(.expanded)>section>ul>li.has-dropdown a' ).on( 'click', function( e ) {
        var menu = $( 'nav.top-bar>section>ul>li.has-dropdown ul' ).foundation( 'dropdown' );
        menu.toggle();
    }
);