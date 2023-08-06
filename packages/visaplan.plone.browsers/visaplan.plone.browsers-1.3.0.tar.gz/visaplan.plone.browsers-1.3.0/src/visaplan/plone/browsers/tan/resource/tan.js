// -*- coding: utf-8 -*- äöü vim: expandtab
$(function () {
  $("#input-start-date").datepicker({
      dateFormat: "dd.mm.yy", // sic - yy ist vierstellig!
      minDate:    0,
      maxDate:    100,
      showOn:     "both",
      buttonImage: "/++resource++unitracc-images/popup_calendar.gif",
      buttonImageOnly: true,
      altField:   '#mirror-date',
      altFormat:  'DD, d.m.yy'
  });
  $("#input-expiration-date").datepicker({
      dateFormat: "dd.mm.yy", // sic - yy ist vierstellig!
      minDate:    0,
      maxDate:    '+2Y',
      showOn:     "both",
      buttonImage: "/++resource++unitracc-images/popup_calendar.gif",
      buttonImageOnly: true,
      altField:   '#mirror-date',
      altFormat:  'DD, d.m.yy'
  });
  $('table.dataTable').dataTable({
      // Tabellenstatus speichern:
      stateSave: true,
      stateDuration: 0, // [s]; 0: unbegrenzt; Vorgabe: 7200 (2h)
      // keinen Fehler ausgeben; die vorstehenden Werte sind
      // ohnehin die Vorgabe lt. Unitracc.datatables_config:
      retrieve: true
  });
})
