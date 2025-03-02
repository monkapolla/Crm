// Инициализация на готовность DOM
document.addEventListener('DOMContentLoaded', function() {
    // Инициализация всплывающих подсказок
    initTooltips();
    
    // Обработка сообщений об ошибках
    initAlertDismiss();
    
    // Форматирование дат
    formatDates();
    
    // Проверка сроков задач
    checkTaskDueDates();
    
    // Добавляем анимации для элементов
    initAnimations();
    
    // Инициализация всплывающих окон (popovers)
    initPopovers();
    
    // Инициализация активных элементов меню
    highlightActiveMenu();
    
    // Сортировка таблиц
    initTableSort();
    
    // Инициализация индикаторов загрузки страницы
    initLoaderIndicator();
    
    // Стилизация форм
    enhanceFormFields();
    
    // Добавляем data-label атрибуты для адаптивных таблиц
    prepareResponsiveTables();
});

// Инициализация всплывающих подсказок Bootstrap
function initTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(function(tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl, {
            delay: { show: 300, hide: 100 }
        });
    });
}

// Инициализация всплывающих окон
function initPopovers() {
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.forEach(function(popoverTriggerEl) {
        new bootstrap.Popover(popoverTriggerEl, {
            trigger: 'hover'
        });
    });
}

// Автоматическое скрытие сообщений
function initAlertDismiss() {
    var alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        // Добавляем анимацию для alert
        alert.classList.add('fade-in');
        
        setTimeout(function() {
            if (alert) {
                // Добавляем анимацию исчезновения
                alert.style.transition = 'opacity 0.5s ease';
                alert.style.opacity = '0';
                
                setTimeout(function() {
                    if (alert && alert.parentNode) {
                        alert.parentNode.removeChild(alert);
                    }
                }, 500);
            }
        }, 5000);
    });
}

// Форматирование дат в человекочитаемый формат
function formatDates() {
    var dateElements = document.querySelectorAll('.format-date');
    dateElements.forEach(function(element) {
        var dateStr = element.textContent.trim();
        if (dateStr) {
            var date = new Date(dateStr);
            if (!isNaN(date)) {
                var options = { 
                    year: 'numeric', 
                    month: 'long', 
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                };
                element.textContent = date.toLocaleString('ru-RU', options);
                
                // Добавляем атрибут с датой для возможной сортировки
                element.setAttribute('data-date', date.getTime());
            }
        }
    });
}

// Проверка сроков задач и подсветка просроченных
function checkTaskDueDates() {
    var taskDueDates = document.querySelectorAll('.task-due-date');
    var now = new Date();
    
    taskDueDates.forEach(function(element) {
        var dateStr = element.getAttribute('data-date');
        if (dateStr) {
            var dueDate = new Date(dateStr);
            if (!isNaN(dueDate)) {
                // Рассчитываем разницу в днях
                var diffTime = dueDate - now;
                var diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
                
                var taskStatus = element.getAttribute('data-status');
                if (taskStatus !== 'Завершена') {
                    if (diffTime < 0) {
                        // Просрочено
                        element.classList.add('task-overdue');
                        element.setAttribute('title', 'Просрочено на ' + Math.abs(diffDays) + ' дней');
                    } else if (diffDays <= 3) {
                        // Скоро наступит срок
                        element.classList.add('text-warning', 'fw-bold');
                        element.setAttribute('title', 'Скоро наступит срок: осталось ' + diffDays + ' дней');
                    }
                }
            }
        }
    });
}

// Добавление анимаций для элементов страницы
function initAnimations() {
    // Анимация для появления карточек
    var cards = document.querySelectorAll('.card');
    cards.forEach(function(card, index) {
        card.classList.add('fade-in');
        card.style.animationDelay = (index * 0.1) + 's';
    });
    
    // Анимация для появления строк таблиц
    var tableRows = document.querySelectorAll('tbody tr');
    tableRows.forEach(function(row, index) {
        row.classList.add('slide-in');
        row.style.animationDelay = (index * 0.05) + 's';
    });
    
    // Анимация для заголовков
    var headings = document.querySelectorAll('h1, h2');
    headings.forEach(function(heading) {
        heading.classList.add('fade-in');
    });
}

// Выделение активного пункта меню
function highlightActiveMenu() {
    var currentPageUrl = window.location.pathname;
    var menuItems = document.querySelectorAll('.navbar-nav .nav-link');
    
    menuItems.forEach(function(item) {
        var itemUrl = item.getAttribute('href');
        if (itemUrl && currentPageUrl.includes(itemUrl) && itemUrl !== '/') {
            item.classList.add('active', 'fw-bold');
            item.setAttribute('aria-current', 'page');
        } else if (itemUrl === '/' && currentPageUrl === '/') {
            item.classList.add('active', 'fw-bold');
            item.setAttribute('aria-current', 'page');
        }
    });
}

// Инициализация сортировки таблиц
function initTableSort() {
    var sortableTables = document.querySelectorAll('.table-sortable');
    
    sortableTables.forEach(function(table) {
        var headers = table.querySelectorAll('th[data-sort]');
        
        headers.forEach(function(header) {
            header.classList.add('sortable');
            header.addEventListener('click', function() {
                var sortField = this.getAttribute('data-sort');
                var tbody = table.querySelector('tbody');
                var rows = Array.from(tbody.querySelectorAll('tr'));
                
                // Определяем направление сортировки
                var isAscending = !this.classList.contains('sort-asc');
                
                // Сбрасываем сортировку для всех заголовков
                headers.forEach(function(h) {
                    h.classList.remove('sort-asc', 'sort-desc');
                });
                
                // Устанавливаем текущее направление сортировки
                if (isAscending) {
                    this.classList.add('sort-asc');
                } else {
                    this.classList.add('sort-desc');
                }
                
                // Сортируем строки
                rows.sort(function(a, b) {
                    var aValue = a.querySelector('td[data-field="' + sortField + '"]').textContent.trim();
                    var bValue = b.querySelector('td[data-field="' + sortField + '"]').textContent.trim();
                    
                    // Проверяем, является ли значение числом
                    if (!isNaN(aValue) && !isNaN(bValue)) {
                        return isAscending ? aValue - bValue : bValue - aValue;
                    } else {
                        return isAscending ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue);
                    }
                });
                
                // Очищаем и заполняем таблицу отсортированными строками
                tbody.innerHTML = '';
                rows.forEach(function(row) {
                    tbody.appendChild(row);
                });
            });
        });
    });
}

// Инициализация индикатора загрузки
function initLoaderIndicator() {
    // Создаем элемент для индикатора загрузки
    var spinnerOverlay = document.createElement('div');
    spinnerOverlay.className = 'spinner-overlay';
    spinnerOverlay.innerHTML = '<div class="spinner-border" role="status"><span class="visually-hidden">Загрузка...</span></div>';
    document.body.appendChild(spinnerOverlay);
    
    // Показываем индикатор при переходе между страницами
    document.addEventListener('click', function(e) {
        var target = e.target;
        
        // Проверяем, является ли клик по ссылке, которая не открывается в новом окне
        if (target.tagName === 'A' && !target.getAttribute('target') && 
            !target.getAttribute('href').startsWith('#') && 
            !target.getAttribute('href').startsWith('javascript:')) {
            spinnerOverlay.style.display = 'flex';
            
            // На всякий случай добавляем таймаут, чтобы скрыть индикатор, если страница не загрузится
            setTimeout(function() {
                spinnerOverlay.style.display = 'none';
            }, 10000);
        }
    });
    
    // Скрываем индикатор при загрузке страницы
    window.addEventListener('load', function() {
        spinnerOverlay.style.display = 'none';
    });
    
    // Показываем индикатор при отправке формы
    document.addEventListener('submit', function(e) {
        var isAjaxForm = e.target.getAttribute('data-ajax') === 'true';
        if (!isAjaxForm) {
            spinnerOverlay.style.display = 'flex';
        }
    });
}

// Улучшение полей форм
function enhanceFormFields() {
    // Автоматическое обновление label для range input
    var rangeInputs = document.querySelectorAll('input[type="range"]');
    rangeInputs.forEach(function(input) {
        var valueDisplay = document.createElement('span');
        valueDisplay.className = 'ms-2 badge bg-primary';
        valueDisplay.textContent = input.value;
        
        input.parentNode.appendChild(valueDisplay);
        
        input.addEventListener('input', function() {
            valueDisplay.textContent = this.value;
        });
    });
    
    // Добавляем счетчик символов для текстовых полей
    var textareas = document.querySelectorAll('textarea[maxlength]');
    textareas.forEach(function(textarea) {
        var maxLength = textarea.getAttribute('maxlength');
        var counter = document.createElement('small');
        counter.className = 'text-muted d-block text-end';
        counter.textContent = textarea.value.length + '/' + maxLength;
        
        textarea.parentNode.insertBefore(counter, textarea.nextSibling);
        
        textarea.addEventListener('input', function() {
            counter.textContent = this.value.length + '/' + maxLength;
            
            // Если близко к максимальному количеству символов
            if (this.value.length > maxLength * 0.9) {
                counter.classList.add('text-danger');
            } else {
                counter.classList.remove('text-danger');
            }
        });
    });
}

// Подготовка таблиц для адаптивного отображения на мобильных устройствах
function prepareResponsiveTables() {
    var tables = document.querySelectorAll('.table');
    tables.forEach(function(table) {
        var headers = table.querySelectorAll('thead th');
        var headerTexts = [];
        
        // Получаем текст из заголовков
        headers.forEach(function(header) {
            headerTexts.push(header.textContent.trim());
        });
        
        // Добавляем data-label атрибуты к ячейкам
        var rows = table.querySelectorAll('tbody tr');
        rows.forEach(function(row) {
            var cells = row.querySelectorAll('td');
            cells.forEach(function(cell, index) {
                if (index < headerTexts.length) {
                    cell.setAttribute('data-label', headerTexts[index]);
                }
            });
        });
    });
} 