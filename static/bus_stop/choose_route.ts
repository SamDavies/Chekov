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
        addButton($(this).text(), chosenDiv, "btn btn-primary");
        $(this).remove();
    });

    chosenDiv.on("click", "button", function() {
        addButton($(this).text(), availableDiv, "btn btn-default");
        $(this).remove();
    });

    function addButton(button: String, div, cssClass){
        var buttonHTML : String = '<button type="button" class="' + cssClass +'">' + button + '</button> ';
        div.prepend(buttonHTML);
    }

    function getName(personid) {
        var dynamicData = {};
        dynamicData["id"] = personid;
        return $.ajax({
            url: "getName.php",
            type: "get",
            data: dynamicData
        });
    }

    getName("2342342").done(function(data) {
        // Updates the UI based the ajax result
        $(".person-name").text(data.name);
    });
}));