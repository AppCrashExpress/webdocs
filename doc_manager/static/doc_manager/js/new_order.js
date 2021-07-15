(function() {
    const rows = document.querySelectorAll("#spec-table tbody tr")
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
                const contains = cells[0].innerText.toLowerCase().includes(from_addr_filter.value) &&
                                 cells[1].innerText.toLowerCase().includes(to_addr_filter.value) &&
                                 cells[2].innerText.toLowerCase().includes(mat_filter.value);
                if (contains) {
                    row.style.display = "";
                } else {
                    row.style.display = "none";
                }
            });
    };

    from_addr_filter.addEventListener('keyup', filter)
    to_addr_filter.addEventListener('keyup', filter)
    mat_filter.addEventListener('keyup', filter)
})()
