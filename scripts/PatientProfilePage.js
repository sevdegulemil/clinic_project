  function validateForm() {
            const name = document.getElementById('input-name').value.trim();
            const email = document.getElementById('input-email').value.trim();
            const saveBtn = document.getElementById('saveToggle');
            saveBtn.disabled = (name === "" || email === "");
        }

        function toggleEdit() {
            document.getElementById('input-name').value = document.getElementById('val-name').innerText;
            document.getElementById('input-email').value = document.getElementById('val-email').innerText;
            document.getElementById('infoDisplay').classList.add('hidden');
            document.getElementById('editToggle').classList.add('hidden');
            document.getElementById('infoEdit').classList.remove('hidden');
            document.getElementById('saveToggle').classList.remove('hidden');
            validateForm();
        }

        function saveChanges() {
            document.getElementById('val-name').innerText = document.getElementById('input-name').value;
            document.getElementById('val-email').innerText = document.getElementById('input-email').value;
            document.getElementById('val-blood').innerText = document.getElementById('input-blood').value;
            document.getElementById('val-gender').innerText = document.getElementById('input-gender').value;
            document.getElementById('infoDisplay').classList.remove('hidden');
            document.getElementById('editToggle').classList.remove('hidden');
            document.getElementById('infoEdit').classList.add('hidden');
            document.getElementById('saveToggle').classList.add('hidden');
        }