// Live availability checking for table selection
const dateInput = document.getElementById('date');
const timeInput = document.getElementById('time');
const availNote = document.getElementById('availNote');

// Set min date to today
const today = new Date().toISOString().split('T')[0];
if (dateInput) dateInput.min = today;

function checkAvailability() {
  const date = dateInput ? dateInput.value : '';
  const time = timeInput ? timeInput.value : '';
  if (!date || !time) return;

  fetch(`/api/availability?date=${date}&time=${time}`)
    .then(res => res.json())
    .then(data => {
      const bookedIds = data.booked_table_ids || [];
      const cards = document.querySelectorAll('.table-card');
      let availCount = 0;

      cards.forEach(card => {
        const radio = card.querySelector('input[type="radio"]');
        const tableId = parseInt(radio.value);
        if (bookedIds.includes(tableId)) {
          card.classList.add('unavailable');
          card.classList.remove('selected');
          radio.checked = false;
        } else {
          card.classList.remove('unavailable');
          availCount++;
        }
      });

      if (availNote) {
        availNote.style.display = 'block';
        if (bookedIds.length === 0) {
          availNote.textContent = `All 8 tables available for this slot.`;
          availNote.style.color = '#2c4a2e';
        } else {
          availNote.textContent = `${availCount} table${availCount !== 1 ? 's' : ''} available — ${bookedIds.length} already booked.`;
          availNote.style.color = '#7a6f5e';
        }
      }
    })
    .catch(() => {});
}

if (dateInput) dateInput.addEventListener('change', checkAvailability);
if (timeInput) timeInput.addEventListener('change', checkAvailability);

// Highlight selected table card
document.querySelectorAll('.table-card').forEach(card => {
  card.addEventListener('click', function () {
    document.querySelectorAll('.table-card').forEach(c => c.classList.remove('selected'));
    if (!this.classList.contains('unavailable')) {
      this.classList.add('selected');
    }
  });
});
