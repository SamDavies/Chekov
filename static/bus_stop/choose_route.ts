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

    /////////////////////////////////
    // The rest of code goes here! //
    /////////////////////////////////
    var chosenRoute: String[] = [];

    var availableDiv: String = $("#available-routes");
    var chosenDiv: String = $("#chosen-routes");

    availableDiv.on("click", "button", function() {
        addButton($(this).text());
        $(this).remove();
    });

    function addButton(button: String){
        var buttonHTML : String = '<button type="button" class="btn btn-primary">' + button + '</button> ';
        chosenDiv.append(buttonHTML);
    }
}));