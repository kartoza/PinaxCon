window.jQuery = window.$ = require("jquery");

require("bootstrap");

require("../less/site.less");

require("../images/foss4g-logo-150px-small.png");


$(document).ready(function() {
    // Display a small box that counts the number of words
    if (Array.prototype.filter) {
        var counter = $(
            '<input type="text" value="0" class="form-control"' +
                'style="float:right;width:3.75em;text-align:right;margin-top:5px" ' +
                'readonly="readonly"/>');
        var textfield = $('#id_abstract');
        textfield.after(counter);

        var charachter_re = /[a-zA-Z0-9]/;
        textfield.on('input propertychange', function(evt) {
            var words = $(this).val().split(/\s+/);
            words = words.filter(function(word) {
                return word.match(charachter_re);
            });
            counter.val(words.length);
        });

        // Populate the field with the current number of words
        textfield.trigger('propertychange');
    }
});
