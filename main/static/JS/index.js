var $input = $('input[name=tags-jquery]')
    .tagify({
            whitelist : [
                "Hello", "How", "are", "you"
            ],
            maxItems: 20,
            dropdown: {
                maxItems: 20,           // <- mixumum allowed rendered suggestions
                classname: "tags-look", // <- custom classname for this dropdown, so it could be targeted
                enabled: 0,             // <- show suggestions on focus
                closeOnSelect: false    // <- do not hide the suggestions dropdown once an item has been selected
            }
        })
        .on('add', function(e, tagName){
            console.log('JQEURY EVENT: ', 'added', tagName)
        })
        .on("invalid", function(e, tagName) {
            console.log('JQEURY EVENT: ',"invalid", e, ' ', tagName);
        });

// get the Tagify instance assigned for this jQuery input object so its methods could be accessed
var jqTagify = $input.data('tagify');

// bind the "click" event on the "remove all tags" button
$('#tags-jquery--removeAllBtn').on('click', jqTagify.removeAllTags.bind(jqTagify))