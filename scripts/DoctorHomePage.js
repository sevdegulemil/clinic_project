
    var calendar;

    document.addEventListener('DOMContentLoaded', function() {
        const datePicker = document.getElementById('datePicker');
        const today = new Date().toISOString().split('T')[0];
   
        datePicker.setAttribute('min', today);
        datePicker.value = today;

        var calendarEl = document.getElementById('calendar');
        calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'timeGridDay',
            locale: 'tr',
            headerToolbar: false,
            allDaySlot: false,
            slotMinTime: '09:00:00',
            slotMaxTime: '18:00:00',
            slotDuration: '00:30:00',
            selectable: true,
            editable: true,
            dayHeaders: false,

            selectAllow: function(selectInfo) {
    
                if (selectInfo.start < new Date()) {
                    return false;
                }

           
                const events = calendar.getEvents();
                return !events.some(event => (selectInfo.start < event.end && selectInfo.end > event.start));
            },
            
            select: function(info) {
                Swal.fire({
                    title: 'Slot Aç',
                    html: `<b>${formatTime(info.start)} - ${formatTime(info.end)}</b> aralığını müsait işaretle?`,
                    icon: 'question',
                    showCancelButton: true,
                    confirmButtonText: 'Evet, Aç',
                    confirmButtonColor: '#f48c06',
                    cancelButtonText: 'İptal'
                }).then((result) => {
                    if (result.isConfirmed) {
                        calendar.addEvent({
                            id: 'slot_' + Date.now(),
                            title: 'Müsait',
                            start: info.start,
                            end: info.end,
                            display: 'background',
                            color: '#E7ECEF'
                        });
                        Swal.fire({ title: 'Başarılı', text: 'Slot açıldı.', icon: 'success', confirmButtonColor: '#f48c06' });
                    }
                });
                calendar.unselect();
            },

            eventClick: function(info) {
                if (info.event.display === 'background') {
                    Swal.fire({
                        title: 'Slotu Kapat?',
                        text: "Müsaitliği kaldırmak istiyor musunuz?",
                        icon: 'question',
                        showCancelButton: true,
                        confirmButtonText: 'Evet, Kapat',
                        confirmButtonColor: '#d33'
                    }).then((result) => {
                        if (result.isConfirmed) info.event.remove();
                    });
                } else {
                    Swal.fire({
                        title: 'Randevu Detayı',
                        html: `<p><strong>Hasta:</strong> ${info.event.title}</p><p><strong>Saat:</strong> ${formatTime(info.event.start)} - ${formatTime(info.event.end)}</p>`,
                        icon: 'info',
                        confirmButtonColor: '#f48c06'
                    });
                }
            },

            events: [
                { id: 'r1', title: 'Ayşe Yılmaz', start: today + 'T10:00:00', end: today + 'T10:30:00', color: '#f48c06', textColor: '#ffffff' },
                { id: 'r2', title: 'Kemal Sunal', start: today + 'T14:30:00', end: today + 'T15:00:00', color: '#f48c06', textColor: '#ffffff' }
            ]
        });

        calendar.render();
        updateRightPanelList();

        datePicker.addEventListener('change', function(e) {
            calendar.gotoDate(e.target.value);
        });
    });

    function updateRightPanelList() {
        const listContainer = document.getElementById('appointmentList');
        const events = calendar.getEvents().filter(e => e.display !== 'background');
        listContainer.innerHTML = ''; 
        events.sort((a, b) => a.start - b.start);
        events.forEach(event => {
            listContainer.innerHTML += `
                <div class="card border-0 shadow-sm mb-2" style="background-color:#f6f9fc; border-left: 5px solid #1a3655 !important;">
                    <div class="card-body p-3">
                        <div class="d-flex justify-content-between mb-1">
                            <span class="badge" style="background-color: #f48c06;">${formatTime(event.start)}</span>
                            <small class="text-muted">Randevu</small>
                        </div>
                        <h6 class="fw-bold mb-1 text-dark">${event.title}</h6>
                        <button class="btn btn-sm btn-outline-danger w-100 rounded-pill mt-2" onclick="cancelFromList('${event.id}')">İptal Et</button>
                    </div>
                </div>`;
        });
    }

    function cancelFromList(eventId) {
        Swal.fire({ title: 'İptal?', icon: 'warning', showCancelButton: true, confirmButtonColor: '#d33', confirmButtonText: 'İptal Et' }).then((result) => {
            if (result.isConfirmed) {
                const event = calendar.getEventById(eventId);
                if (event) { event.remove(); updateRightPanelList(); }
            }
        });
    }

    function formatTime(date) { return date.toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' }); }
    function toggleChat() { document.getElementById('pagerChat').classList.toggle('open'); }
    function sendMessage() {
        const input = document.getElementById('chatInput');
        if(!input.value) return;
        document.getElementById('chatBody').innerHTML += `<div class="d-flex mb-3 flex-row-reverse"><div class="text-white p-2 rounded small" style="background-color: #f48c06;">${input.value}</div></div>`;
        input.value = '';
    }
