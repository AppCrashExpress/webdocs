(function() {
    const rows = document.querySelectorAll("#spec-table tbody tr")
    const client_filter    = document.querySelector("#client-filter")
    const from_addr_filter = document.querySelector("#from-addr-filter")
    const to_addr_filter   = document.querySelector("#to-addr-filter")
    const mat_filter       = document.querySelector("#mat-filter")
    let prev_row = null;

    rows.forEach(function (row) {
        const row_radio = row.querySelector('input');

        row.addEventListener("click", (event) => {
            row_radio.checked = true;
            row.classList.add('table-info');
            if (prev_row && prev_row != row) {
                prev_row.classList.remove('table-info');
            }
            prev_row = row;
        })
    })

    filter = function () {
            rows.forEach(function (row) {
                const cells = row.querySelectorAll("td");
                const contains = cells[0].innerText.toUpperCase().includes(client_filter.value.toUpperCase()) &&
                                 cells[1].innerText.toUpperCase().includes(from_addr_filter.value.toUpperCase()) &&
                                 cells[2].innerText.toUpperCase().includes(to_addr_filter.value.toUpperCase()) &&
                                 cells[3].innerText.toUpperCase().includes(mat_filter.value.toUpperCase());
                if (contains) {
                    row.style.display = "";
                } else {
                    row.style.display = "none";
                }
            });
    };

    client_filter.addEventListener('keyup', filter)
    from_addr_filter.addEventListener('keyup', filter)
    to_addr_filter.addEventListener('keyup', filter)
    mat_filter.addEventListener('keyup', filter)
})()

$(document).ready(function() {
        // Allow of only one select element
    $('#id_driver').on('select2:select', function (e) { $('#id_contractor').val('').trigger('change') } );

    $('#id_contractor').on('select2:select', function (e) { 
        $('#id_driver').val('').trigger('change');
        $('#id_vehicle').val('').trigger('change');
    });
})
