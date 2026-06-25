document.addEventListener('DOMContentLoaded', function () {
  const avatarInputs = document.querySelectorAll('.team-upload-input');

  function updateAvatar(avatarEl, imageDataUrl) {
    if (!avatarEl) return;
    avatarEl.style.backgroundImage = `url('${imageDataUrl}')`;
    avatarEl.classList.add('has-image');
    avatarEl.textContent = '';
  }

  function loadSavedAvatars() {
    avatarInputs.forEach((input) => {
      const avatarKey = `team-avatar-${input.dataset.teamAvatar}`;
      const savedData = localStorage.getItem(avatarKey);
      if (savedData) {
        const avatarEl = document.querySelector(`.team-avatar[data-initials="${input.dataset.teamAvatar}"]`);
        updateAvatar(avatarEl, savedData);
      }
    });
  }

  avatarInputs.forEach((input) => {
    input.addEventListener('change', function (event) {
      const file = event.target.files[0];
      if (!file || !file.type.startsWith('image/')) return;

      const reader = new FileReader();
      reader.onload = function (e) {
        const dataUrl = e.target.result;
        const avatarEl = document.querySelector(`.team-avatar[data-initials="${input.dataset.teamAvatar}"]`);
        updateAvatar(avatarEl, dataUrl);
        localStorage.setItem(`team-avatar-${input.dataset.teamAvatar}`, dataUrl);
      };
      reader.readAsDataURL(file);
    });
  });

  loadSavedAvatars();
});