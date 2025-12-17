 var calendar;

    document.addEventListener('DOMContentLoaded', function() {
        const today = new Date().toISOString().split('T')[0];
        const datePicker = document.getElementById('datePicker');
        datePicker.setAttribute('min', today);
        datePicker.value = today;

        var calendarEl = document.getElementById('calendar');
        calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'timeGridDay',
            locale: 'tr',
            headerToolbar: false,
            allDaySlot: false,
            dayHeaders: false,
            slotMinTime: '10:00:00',
            slotMaxTime: '18:00:00',
            slotDuration: '00:30:00',
            selectable: false,
            selectOverlap: false,
            editable: false,
            eventDurationEditable: false,
            initialDate: today,
            
            select: function(info) {
                if (info.start < new Date()) {
                      Swal.fire({ 
                    title: 'Hata', 
                    text: 'Geçmiş bir zamana randevu alamazsınız.', 
                    icon: 'error',
                    confirmButtonText: 'Tamam',
                    confirmButtonColor: '#f48c06' 
                });
                    calendar.unselect();
                    return;
                }

                const currentEvents = calendar.getEvents().filter(e => e.display !== 'background');
                if (currentEvents.length > 0) {
                      Swal.fire({ 
                    title: 'Hata', 
                    text: 'Aynı gün için sadece 1 randevu alabilirsiniz.', 
                    icon: 'error',
                    confirmButtonText: 'Tamam',
                    confirmButtonColor: '#f48c06' 
                });
                    calendar.unselect();
                    return;
                }

                let selectedStart = info.start;
                let selectedEnd = info.end;
                if ((selectedEnd - selectedStart) > 1800000) {
                    selectedEnd = new Date(selectedStart.getTime() + 1800000);
                }

                Swal.fire({
                    title: 'Randevu Onayı',
                    html: `Seçilen Saat: <b>${formatTime(selectedStart)} - ${formatTime(selectedEnd)}</b>`,
                    showCancelButton: true,
                    confirmButtonText: 'Evet, Onayla',
                    confirmButtonColor: '#f48c06',
                    cancelButtonText: 'Vazgeç'
                }).then((result) => {
                    if (result.isConfirmed) {
                        calendar.addEvent({
                            id: Date.now().toString(),
                            title: 'Randevum',
                            start: selectedStart,
                            end: selectedEnd,
                            color: '#f48c06', 
                            textColor: '#ffffff'
                        });
                        Swal.fire({ title: 'Başarılı', text: 'Randevunuz oluşturuldu.', icon: 'success', confirmButtonColor: '#f48c06' });
                        updateRightPanel();
                    }
                });
                calendar.unselect();
            }
        });
        calendar.render();
    });

    const doctorsData = {
        'genel': ['Dr. Ayşenur Mayuk', 'Dr. Eren Yıldız', 'Dr. İlknur Tulgar'],
        'cocuk': ['Dr. Sevde Gül Emil']
    };

    function updateDoctors() {
        const branch = document.getElementById('branchSelect').value;
        const doctorSelect = document.getElementById('doctorSelect');
        doctorSelect.innerHTML = '<option value="">Doktor Seçiniz...</option>';
        doctorSelect.disabled = false;
        if (doctorsData[branch]) {
            doctorsData[branch].forEach(doc => {
                doctorSelect.add(new Option(doc, doc));
            });
        }
    }

    function filterAppointments() {
        const docName = document.getElementById('doctorSelect').value;
        const selectedDate = document.getElementById('datePicker').value;
        
        if(!docName) {
          Swal.fire({ 
            title: 'Uyarı', 
            text: 'Lütfen bir doktor seçiniz.', 
            icon: 'warning',
            confirmButtonText: 'Tamam',
            confirmButtonColor: '#f48c06' 
        });
            return;
        }

        calendar.gotoDate(selectedDate);
        calendar.setOption('selectable', true);
        calendar.removeAllEvents();

        calendar.addEvent({
            title: 'Dolu',
            start: selectedDate + 'T12:00:00',
            end: selectedDate + 'T13:00:00',
            display: 'background',
            color: '#cccccc'
        });

        document.getElementById('calendarTitle').innerText = `${docName} - Müsaitlik`;
        document.getElementById('calendarSubtitle').innerText = "Boş slotlara tıklayarak randevu oluşturabilirsiniz.";
        Swal.fire({ icon: 'success', title: 'Slotlar Güncellendi', timer: 800, showConfirmButton: false });
    }

    function updateRightPanel() {
        const listContainer = document.getElementById('activeAppointmentsList');
        const events = calendar.getEvents().filter(e => e.display !== 'background');
        listContainer.innerHTML = ''; 
        if (events.length === 0) {
            listContainer.innerHTML = `<div class="text-center text-muted mt-5"><i class="bi bi-calendar-x fs-1 opacity-50"></i><p class="mt-2 small">Randevu yok.</p></div>`;
            return;
        }
        events.forEach(event => {
            const docName = document.getElementById('doctorSelect').value || 'Seçili Doktor';
            listContainer.innerHTML += `
                <div class="card border-0 shadow-sm" style="background-color: #f6f9fc; border-left: 5px solid #3b5173 !important;">
                    <div class="card-body p-3">
                        <div class="d-flex justify-content-between mb-2">
                            <span class="badge" style="background-color: #f48c06;">Aktif</span>
                            <small class="fw-bold text-muted">${formatDate(event.start)}</small>
                        </div>
                        <h6 class="fw-bold mb-1">${docName}</h6>
                        <p class="small fw-bold mb-3"><i class="bi bi-clock me-1"></i>${formatTime(event.start)} - ${formatTime(event.end)}</p>
                        <button class="btn btn-sm btn-outline-danger w-100 rounded-pill" onclick="cancelAppointment('${event.id}')">İptal Et</button>
                    </div>
                </div>`;
        });
    }

    function cancelAppointment(eventId) {
        Swal.fire({ title: 'İptal?', text: "Randevu silinecek.", icon: 'warning', showCancelButton: true, confirmButtonColor: '#d33', confirmButtonText: 'Sil' }).then((result) => {
            if (result.isConfirmed) {
                calendar.getEventById(eventId).remove();
                updateRightPanel();
            }
        });
    }

    function formatTime(date) { return date.toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' }); }
    function formatDate(date) { return date.toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' }); }
    function toggleChat() { document.getElementById('pagerChat').classList.toggle('open'); }
    function sendMessage() {
        const input = document.getElementById('chatInput');
        const body = document.getElementById('chatBody');
        if(!input.value) return;
        body.innerHTML += `<div class="d-flex mb-3 flex-row-reverse"><div class="text-white p-2 rounded small" style="background-color: #f48c06;">${input.value}</div></div>`;
        input.value = '';
        body.scrollTop = body.scrollHeight;
    }