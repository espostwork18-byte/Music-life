(function () {
  var form = document.getElementById('contact-form');
  if (!form) return;
  var status = document.getElementById('form-status');

  var en = document.documentElement.lang === 'en';
  var messages = en ? {
    name: 'Please enter your full name.',
    email: 'Please enter a valid email address.',
    org: 'Please enter your company or organisation.',
    area: 'Please select an area of interest.',
    message: 'Please write a short message.',
    consent: 'Please confirm you have read the Privacy Policy.'
  } : {
    name: 'Inserisci nome e cognome.',
    email: 'Inserisci un indirizzo email valido.',
    org: 'Indica azienda o organizzazione.',
    area: 'Seleziona un’area di interesse.',
    message: 'Scrivi un breve messaggio.',
    consent: 'Conferma di aver letto la Privacy Policy.'
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
      status.textContent = en ? 'Please check the highlighted fields.' : 'Controlla i campi evidenziati.';
      var el = form.querySelector('[data-field="' + bad + '"] input, [data-field="' + bad + '"] textarea');
      if (el) el.focus();
      return;
    }
    status.textContent = en ? 'Thank you for writing to us. We will get back to you as soon as possible.' : 'Grazie per averci scritto. Ti risponderemo al più presto.';
    var note = document.createElement('span');
    note.className = 'form__note';
    note.textContent = en ? 'Site preview: the form is not yet connected to the company inbox.' : 'Anteprima del sito: l’invio non è ancora collegato alla casella email aziendale.';
    status.appendChild(note);
    form.reset();
  });
})();
