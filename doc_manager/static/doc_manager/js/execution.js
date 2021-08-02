$(document).ready(function() {
    const spec_filter       = $("#spec-id-filter");
    const customer_filter   = $("#customer-filter");
    const start_date_filter = $("#start-date-filter");
    const end_date_filter   = $("#end-date-filter");

    $("#order-table tbody tr").each(function() {
        const row   = $(this);
        const input = row.find("input");
        
        // If already checked, mark the column
        if (input.is(":checked")) {
            row.addClass("table-info");
        }

        // Disable direct input
        input.click(function () { 
            input[0].checked = !input[0].checked;
        })

        row.click(function () {
            row.toggleClass("table-info");
            input[0].checked = !input[0].checked;
        })
    })

    filter = function() {
        $("#order-table tbody tr").each(function () {
            const row = $(this);
            const cells = row.find("td");
            const contains = (cells[3].innerText.toLowerCase() === spec_filter.val() 
                                || !spec_filter.val() ) &&
                             cells[6].innerText.toLowerCase().includes(customer_filter.val());

            let start_date;
            let end_date;
            let curr_date;
            if (start_date_filter.val()) {
                start_date = Date.parse(start_date_filter.val());
            } else {
                start_date = Date.parse(cells[0].innerText);
            }
            if (end_date_filter.val()) {
                end_date = Date.parse(end_date_filter.val());
            } else {
                end_date = Date.parse(cells[0].innerText);
            }
            curr_date  = Date.parse(cells[0].innerText);

            const in_range = curr_date >= start_date &&
                             curr_date <= end_date;

            if (contains && in_range) {
                row.show();
            } else {
                row.hide();
            }
        });
    }

    spec_filter.keyup(filter);
    customer_filter.keyup(filter);
    start_date_filter.change(filter);
    end_date_filter.change(filter);
})
