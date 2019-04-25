var REIMBURSEMENTS = REIMBURSEMENTS || {};

REIMBURSEMENTS.populateMonthDropdown = function() {
	// Calculate the options for month from the given start and end months and years
	var $reimbursement_school_year_selected = $('#reimbursement-school-year').find(':selected'),
		$reimbursement_dropdown_cell = $('#reimbursement-month-dropdown-cell'),
		start_month = $reimbursement_school_year_selected.data('start-month'),
		start_year = $reimbursement_school_year_selected.data('start-year'),
		end_month = $reimbursement_school_year_selected.data('end-month'),
		end_year = $reimbursement_school_year_selected.data('end-year');

	$reimbursement_dropdown_cell.html(BASE.generateYearMonthDropdown(start_year, end_year, start_month, end_month));
};

$(document).ready(function(){
	REIMBURSEMENTS.populateMonthDropdown();
	$(document)
		.on('change', '#reimbursement-school-year', REIMBURSEMENTS.populateMonthDropdown);
});