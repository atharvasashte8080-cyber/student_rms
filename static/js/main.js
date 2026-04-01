// ============================================================
// Student Record Management System — Main JS
// ============================================================

// ─── DATE IN TOPBAR ──────────────────────────────────────────
function updateTopbarDate() {
  const el = document.getElementById('topbarDate');
  if (!el) return;
  const now = new Date();
  const opts = { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' };
  el.textContent = now.toLocaleDateString('en-IN', opts);
}

// ─── SIDEBAR TOGGLE ──────────────────────────────────────────
function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  if (sidebar) sidebar.classList.toggle('open');
}

// Close sidebar when clicking outside on mobile
document.addEventListener('click', (e) => {
  const sidebar = document.getElementById('sidebar');
  const toggle  = document.getElementById('menuToggle');
  if (!sidebar) return;
  if (window.innerWidth <= 768 && sidebar.classList.contains('open')) {
    if (!sidebar.contains(e.target) && !toggle.contains(e.target)) {
      sidebar.classList.remove('open');
    }
  }
});

// ─── AUTO-DISMISS FLASH MESSAGES ─────────────────────────────
function setupFlashAutoDismiss() {
  const flashes = document.querySelectorAll('.flash');
  flashes.forEach((flash, i) => {
    setTimeout(() => {
      flash.style.transition = 'opacity 0.4s';
      flash.style.opacity = '0';
      setTimeout(() => flash.remove(), 400);
    }, 4000 + i * 500);
  });
}

// ─── FORM VALIDATION HELPERS ─────────────────────────────────
function setupForms() {
  const forms = document.querySelectorAll('form[novalidate]');
  forms.forEach(form => {
    form.addEventListener('submit', (e) => {
      const required = form.querySelectorAll('[required]');
      let valid = true;
      required.forEach(field => {
        field.style.borderColor = '';
        if (!field.value.trim()) {
          field.style.borderColor = 'var(--red)';
          valid = false;
        }
      });
      if (!valid) {
        e.preventDefault();
        const first = form.querySelector('[required]:not([value]), [required][value=""]');
        if (first) first.focus();
      }
    });
  });
}

// ─── ANIMATE STAT NUMBERS ────────────────────────────────────
function animateNumbers() {
  const values = document.querySelectorAll('.stat-value');
  values.forEach(el => {
    const target = parseInt(el.textContent, 10);
    if (isNaN(target)) return;
    let current = 0;
    const step  = Math.ceil(target / 30);
    const timer = setInterval(() => {
      current += step;
      if (current >= target) {
        el.textContent = target;
        clearInterval(timer);
      } else {
        el.textContent = current;
      }
    }, 20);
  });
}

// ─── ANIMATE DEPT BARS ───────────────────────────────────────
function animateBars() {
  const bars = document.querySelectorAll('.dept-bar-fill');
  bars.forEach(bar => {
    const target = bar.style.width;
    bar.style.width = '0';
    setTimeout(() => { bar.style.width = target; }, 200);
  });
}

// ─── INIT ─────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  updateTopbarDate();
  setupFlashAutoDismiss();
  setupForms();
  animateNumbers();
  animateBars();
});

function confirmDelete(btn) {
    const id = btn.dataset.id;
    const name = btn.dataset.name;
    console.log(id, name);
}