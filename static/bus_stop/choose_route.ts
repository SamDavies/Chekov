// IIFE - Immediately Invoked Function Expression
(function(yourcode) {

    // The global jQuery object is passed as a parameter
    yourcode(window.jQuery, window, document);

}(function($, window, document) {

    // The $ is now locally scoped

    // Listen for the jQuery ready event on the document
    $(function() {
        console.log('The DOM is ready');
        // The DOM is ready!
    });

    console.log('The DOM may not be ready');

    // The rest of code goes here!
    var list = $("#available-routes");

    list.on("mouseenter", "button", function(){
        $(this).text("Click me!");
    });

    list.on("click", "button", function() {
        $(this).text("Why did you click me?!");
    });
}));