(function () {
  var form = document.getElementById('contact-form');
  if (!form) return;
  var status = document.getElementById('form-status');

  var messages = {
    name: 'Inserisci nome e cognome.',
    email: 'Inserisci un indirizzo email valido.',
    org: 'Indica azienda o organizzazione.',
    area: 'Seleziona un’area di interesse.',
    message: 'Scrivi un breve messaggio.',
    consent: 'Il consenso è necessario per inviare il messaggio.'
  };

  function setError(key, bad) {
    var field = form.querySelector('[data-field="' + key + '"]');
    if (!field) return;
    if (bad) field.setAttribute('data-invalid', ''); else field.removeAttribute('data-invalid');
    var err = field.querySelector('.field__error');
    if (err) err.textContent = bad ? messages[key] : '';
  }

  function validate() {
    var v = {
      name: form.elements.name.value.trim().length > 1,
      email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.elements.email.value.trim()),
      org: form.elements.org.value.trim().length > 1,
      area: !!form.querySelector('input[name="area"]:checked'),
      message: form.elements.message.value.trim().length > 4,
      consent: form.elements.consent.checked
    };
    var firstBad = null;
    Object.keys(v).forEach(function (k) {
      setError(k, !v[k]);
      if (!v[k] && !firstBad) firstBad = k;
    });
    return firstBad;
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var bad = validate();
    if (bad) {
      status.textContent = 'Controlla i campi evidenziati.';
      var el = form.querySelector('[data-field="' + bad + '"] input, [data-field="' + bad + '"] textarea');
      if (el) el.focus();
      return;
    }
    status.textContent = 'Grazie per averci scritto. Ti risponderemo al più presto.';
    var note = document.createElement('span');
    note.className = 'form__note';
    note.textContent = 'Anteprima del sito: l’invio non è ancora collegato alla casella email aziendale.';
    status.appendChild(note);
    form.reset();
  });
})();
