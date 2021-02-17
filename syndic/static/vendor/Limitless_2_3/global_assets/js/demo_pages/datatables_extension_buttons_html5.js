/* ------------------------------------------------------------------------------
 *
 *  # Buttons extension for Datatables. HTML5 examples
 *
 *  Demo JS code for datatable_extension_buttons_html5.html page
 *
 * ---------------------------------------------------------------------------- */
function getBase64ImageFromURL(url) {
    return new Promise((resolve, reject) => {
      var img = new Image();
      img.setAttribute("crossOrigin", "anonymous");
      img.onload = () => {
        var canvas = document.createElement("canvas");
        canvas.width = img.width;
        canvas.height = img.height;
        var ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0);
        var dataURL = canvas.toDataURL("image/png");
        resolve(dataURL);
      };
      img.onerror = error => {
        reject(error);
      };
      img.src = url;
    });
  }
//console.log(this.getBase64ImageFromURL('/static/images/logo_n3.png'))
// Setup module
// ------------------------------

var DatatableButtonsHtml5 = function() {


    //
    // Setup module components
    //

    // Basic Datatable examples
    var _componentDatatableButtonsHtml5 = function() {
        if (!$().DataTable) {
            console.warn('Warning - datatables.min.js is not loaded.');
            return;
        }

        // Setting datatable defaults
        $.extend( $.fn.dataTable.defaults, {
            autoWidth: false,
            dom: '<"datatable-header"fBl><"datatable-scroll-wrap"t><"datatable-footer"ip>',
            language: {
                search: '<span>Filter:</span> _INPUT_',
                searchPlaceholder: 'Type to filter...',
                lengthMenu: '<span>Show:</span> _MENU_',
                paginate: { 'first': 'First', 'last': 'Last', 'next': $('html').attr('dir') == 'rtl' ? '&larr;' : '&rarr;', 'previous': $('html').attr('dir') == 'rtl' ? '&rarr;' : '&larr;' }
            }
        });


        // Basic initialization
        $('.datatable-button-html5-basic').DataTable({
            buttons: {            
                dom: {
                    button: {
                        className: 'btn btn-light'
                    }
                },
                buttons: [
                    'copyHtml5',
                    'excelHtml5',
                    'csvHtml5',
                    'pdfHtml5'
                ]
            }
        });


        // PDF with image
        $('.datatable-button-html5-image').DataTable({
            buttons: [
                {
                    extend: 'pdfHtml5',
                    text: 'Export to PDF <i class="icon-file-pdf ml-2"></i>',
                    className: 'btn bg-teal-400',
                    customize: function (doc) {
                        doc.content.splice(1, 0, {
                            margin: [0, 0, 0, 12],
                            alignment: 'center',
                            fontFamily: 'Helvetica',
                            // image: 'data:image/png;base64,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'
                        });
                    }
                }
            ]
        });


        // Column selectors
        $('.datatable-button-html5-columns').DataTable({
            buttons: {            
                buttons: [
                    {
                        extend: 'copyHtml5',
                        text: 'Copy <i class="icon-copy3 ml-2"></i>',
                        className: 'btn bg-blue-300',
                        exportOptions: {
                            columns: [ 0, ':visible' ]
                        }
                    },
                    {
                        extend: 'excelHtml5',
                        text: 'Excel <i class="icon-file-excel ml-2"></i>',
                        className: 'btn bg-teal-300',
                        exportOptions: {
                            columns: ':visible'
                        }
                    },
                    {
                        extend: 'pdfHtml5',
                        text: 'PDF <i class="icon-file-pdf ml-2" ></i>',
                        className: 'btn bg-grey-300',
                        exportOptions: {
                            columns: [0, 1, 2, 3, 4]
                        },

                        customize: function (doc) {
                        doc.content.splice(1, 0, {
                            margin: [2, 0, 0, 12],
                            // footer: {
                            //     columns: [
                            //         'Left part',
                            //         { text: 'Edussy.com', alignment: 'right' }
                            //     ]
                            // },
                            alignment: 'center',
                            fontFamily: 'Helvetica',

                                image: 'data:image/png;base64,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',
                                width: 83,
                            height:45

                        });
                    }
                    },
                    {
                        extend: 'colvis',
                        text: '<i class="icon-three-bars"></i>',
                        className: 'btn bg-blue btn-icon dropdown-toggle'
                    }
                ]
            }

        });


        // Tab separated values
        $('.datatable-button-html5-tab').DataTable({
            buttons: {            
                buttons: [
                    {
                        extend: 'copyHtml5',
                        className: 'btn btn-light',
                        text: '<i class="icon-copy3 mr-2"></i> Copy'
                    },
                    {
                        extend: 'csvHtml5',
                        className: 'btn btn-light',
                        text: '<i class="icon-file-spreadsheet mr-2"></i> CSV',
                        fieldSeparator: '\t',
                        extension: '.tsv'
                    }
                ]
            }
        });
    };

    // Select2 for length menu styling
    var _componentSelect2 = function() {
        if (!$().select2) {
            console.warn('Warning - select2.min.js is not loaded.');
            return;
        }

        // Initialize
        $('.dataTables_length select').select2({
            minimumResultsForSearch: Infinity,
            dropdownAutoWidth: true,
            width: 'auto'
        });
    };


    //
    // Return objects assigned to module
    //

    return {
        init: function() {
            _componentDatatableButtonsHtml5();
            _componentSelect2();
        }
    }
}();


// Initialize module
// ------------------------------

document.addEventListener('DOMContentLoaded', function() {
    DatatableButtonsHtml5.init();
});

