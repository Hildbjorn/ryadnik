console.log(`Copyright (c) 2024 Artem Fomin`);

// CSRF токен для работы HTMX
document.addEventListener('htmx:configRequest', function (event) {
    var csrfToken = document.querySelector('meta[name="csrfmiddlewaretoken"]').content;
    if (csrfToken) {
        event.detail.headers['X-CSRFToken'] = csrfToken;
    } else {
        console.error("CSRF Token not found in meta tag.");
    }
});

// Функция для проверки, является ли текущая ширина экрана маленькой
function isSmallScreen() {
    return window.innerWidth < 1200;
}
const navLinks = document.querySelectorAll('.nav-item');
const menuToggle = document.querySelector('#offcanvasNavbar');
if (navLinks.length > 0) {
    if (isSmallScreen()) {
        navLinks.forEach((elem) => {
            elem.addEventListener('click', (event) => {
                if (!event.target.classList.contains('dropdown-toggle')) {
                    $("button.navbar-toggler").click();
                }
            });
        });
    }
    window.addEventListener('resize', () => {
        if (isSmallScreen()) {
            navLinks.forEach((elem) => {
                elem.addEventListener('click', (event) => {
                    if (!event.target.classList.contains('dropdown-toggle')) {
                        $("button.navbar-toggler").click();
                    }
                });
            });
        } else {
            navLinks.forEach((elem) => {
                elem.removeEventListener('click', (event) => {
                    if (!event.target.classList.contains('dropdown-toggle')) {
                        $("button.navbar-toggler").click();
                    }
                });
            });
        }
    });
}

document.addEventListener('DOMContentLoaded', function () {
    // Инициализация popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Инициализация tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});


// Установка прозрачности меню при прокрутке страницы
document.addEventListener('scroll', function () {
    const navbar = document.querySelector('nav.navbar');
    if (window.scrollY > 60) {
        navbar.classList.add('transparent');
    } else {
        navbar.classList.remove('transparent');
    }
});

// Включение экрана со спинером загрузки
function initializeSpinnerAndButtons() {
    const buttons = document.querySelectorAll(".btn_submit");
    const spinner = document.getElementById("spinner");
    const forms = document.querySelectorAll("form");

    // Скрываем спиннер и разблокируем тело документа при загрузке
    spinner.style.display = "none";
    document.body.classList.remove('lock');

    // Проверяем наличие кнопок на странице
    if (buttons.length === 0) {
        return;
    }

    buttons.forEach(button => {
        button.addEventListener("click", function (event) {
            console.log("Кнопка нажата")
            let hasErrors = false;
            forms.forEach(form => {
                if (form.checkValidity() === false) {
                    hasErrors = true;
                    return;
                }
            });
            if (hasErrors) {
                return;
            }
            spinner.style.display = "flex";
            document.body.classList.add('lock');
        });
    });
}
document.addEventListener("DOMContentLoaded", initializeSpinnerAndButtons);

// Выключение экрана со спинером загрузки
function hideSpinner() {
    const spinner = document.getElementById("spinner");
    spinner.style.display = "none";
    document.body.classList.remove('lock');
}

// Закрытие сообщений через проведуток времени
function showAlertMessages(delay = 5000) { // Задержка по умолчанию 5 секунд
    const alertMessages = document.querySelector('.alert_messages');
    if (alertMessages) {
        alertMessages.classList.add('show'); // Добавляем класс show для плавного появления
        // Установите таймер на delay миллисекунд для исчезновения сообщения
        setTimeout(() => {
            alertMessages.classList.remove('show'); // Убираем класс show для плавного исчезновения
        }, delay);
        // Обработчик события для кнопки закрытия
        const closeButtons = document.querySelectorAll('.btn-close');
        closeButtons.forEach(button => {
            button.addEventListener('click', () => {
                alertMessages.classList.remove('show'); // Убираем класс show при нажатии кнопки закрытия
            });
        });
    }
}
// Вызов функции
document.addEventListener('DOMContentLoaded', function () {
    showAlertMessages(5000); // Вы можете указать другую задержку в миллисекундах
});


// Установка высоты #header_plug равной максимальной высоте между header и nav.navbar.
document.addEventListener("DOMContentLoaded", function () {
    const htmlElem = document.querySelector('html');
    const navbar = document.querySelector('nav.navbar');
    const header = document.querySelector('header');
    const headerPlug = document.getElementById('header_plug');
    const heroSection = document.getElementById('hero');

    function setHeaderPlugHeight() {
        const navbarHeight = navbar ? navbar.offsetHeight : 0;
        const headerHeight = header ? header.offsetHeight : 0;
        const maxHeight = Math.max(navbarHeight, headerHeight);

        // Устанавливаем высоту для header_plug
        if (headerPlug) {
            headerPlug.style.height = maxHeight + 'px';
        }

        // Устанавливаем scroll-padding-top для htmlElem
        htmlElem.style.scrollPaddingTop = maxHeight + 'px';

        // Устанавливаем высоту для heroSection
        if (heroSection) {
            heroSection.style.height = `calc(100vh - ${maxHeight}px)`;
        }
    }

    // Устанавливаем высоту и scroll-padding при загрузке страницы
    setHeaderPlugHeight();

    // Устанавливаем высоту и scroll-padding при изменении размера окна
    window.addEventListener('resize', setHeaderPlugHeight);
});

// Установка высоты project_description_col равной высоте изображения.
window.addEventListener('load', function () {
    const imagePreview = document.getElementById('image_preview');
    const projectDescriptionCol = document.querySelector('.project_description_col');
    if (imagePreview && projectDescriptionCol) {
        function setEqualHeight() {
            if (window.innerWidth >= 992) {
                const imageHeight = imagePreview.offsetHeight;
                projectDescriptionCol.style.setProperty('height', imageHeight + 'px', 'important');
            } else {
                projectDescriptionCol.style.removeProperty('height');
            }
        }
        setEqualHeight();
        window.addEventListener('resize', setEqualHeight);
        document.addEventListener('click', setEqualHeight);
    }
});

// Загрузка Обложки
document.addEventListener('DOMContentLoaded', function () {
    // Получаем контейнер аватара по ID
    const imagePreview = document.getElementById('image_preview');

    if (imagePreview) {
        // Находим input для загрузки файла внутри контейнера
        const imageInput = imagePreview.querySelector('input[type="file"][name="image"]');
        // Находим элемент img для предпросмотра
        const img = imagePreview.querySelector('img');

        if (imageInput && img) {
            imageInput.addEventListener('change', function (event) {
                const file = event.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = function (e) {
                        img.src = e.target.result; // Обновляем источник изображения
                        img.style.display = 'block'; // Убеждаемся, что изображение отображается
                    }
                    reader.readAsDataURL(file); // Читаем файл как Data URL
                } else {
                    img.style.display = 'none'; // Опционально: скрыть изображение, если файл не выбран
                }
            });
        }
    }
});

// Автозаполнение поля "Организация"
document.addEventListener("DOMContentLoaded", function () {
    findCompany();
});

document.addEventListener("htmx:afterSwap", function (event) {
    findCompany();
});

function findCompany() {
    let companyField = document.querySelectorAll('.company_field');

    // Проверка наличия элементов .company_field
    if (companyField.length === 0) {
        return;
    }

    $(companyField).suggestions({
        token: "96e2dc70ca88016a7ab1e758ecd29864cd1e981d",
        type: "PARTY",
        // Вызывается, когда пользователь выбирает одну из подсказок
        onchange: function (suggestion) {
        }
    });
}

// Маска ввода номера телефона
// Инициализация при загрузке страницы
document.addEventListener("DOMContentLoaded", function () {
    initializePhoneMask();
});

// Инициализация после подгрузки элементов HTMX
document.addEventListener("htmx:afterSwap", function (event) {
    initializePhoneMask();
});

function initializePhoneMask() {
    const inputs = document.querySelectorAll('.tel');

    // Проверяем, есть ли элементы с классом .tel
    if (inputs.length > 0) {
        [].forEach.call(inputs, function (input) {
            let keyCode;

            function mask(event) {
                event.keyCode && (keyCode = event.keyCode);
                let pos = this.selectionStart;
                if (pos < 3) event.preventDefault();
                let matrix = "+7 (___) ___ ____",
                    i = 0,
                    def = matrix.replace(/\D/g, ""),
                    val = this.value.replace(/\D/g, ""),
                    new_value = matrix.replace(/[_\d]/g, function (a) {
                        return i < val.length ? val.charAt(i++) || def.charAt(i) : a;
                    });
                i = new_value.indexOf("_");
                if (i != -1) {
                    i < 5 && (i = 3);
                    new_value = new_value.slice(0, i);
                }
                let reg = matrix.substr(0, this.value.length).replace(/_+/g,
                    function (a) {
                        return "\\d{1," + a.length + "}";
                    }).replace(/[+()]/g, "\\$&");
                reg = new RegExp("^" + reg + "$");
                if (!reg.test(this.value) || this.value.length < 5 || keyCode > 47 && keyCode < 58) this.value = new_value;
                if (event.type == "blur" && this.value.length < 5) this.value = "";
            }

            input.addEventListener("input", mask, false);
            input.addEventListener("focus", mask, false);
            input.addEventListener("blur", mask, false);
            input.addEventListener("keydown", mask, false);
        });
    }
}

// Анимация Hero
window.onload = function () {
    const animatedElement = document.querySelector('.animated');
    const animations = ['move-up', 'move-down', 'move-left', 'move-right'];

    if (animatedElement) {
        function randomAnimation() {
            const randomIndex = Math.floor(Math.random() * animations.length);
            const animationClass = animations[randomIndex];

            // Удаляем предыдущую анимацию, если она есть
            animatedElement.classList.remove(...animations);

            // Запускаем новую анимацию
            animatedElement.classList.add(animationClass);

            // Возвращаем элемент в исходное положение после завершения анимации
            setTimeout(() => {
                animatedElement.classList.remove(animationClass); // Убираем класс движения
            }, 2000); // Длительность анимации (2 секунды)
        }

        // Запускаем функцию каждые 1 секунду
        setInterval(randomAnimation, 1000);
    }
};

// Асинхронная обработка форм
$(document).ready(function () {
    bindAjaxForms();

    function bindAjaxForms() {
        $('form.ajax-form').on('submit', function (event) {
            event.preventDefault();
            const $form = $(this);
            const formId = $form.attr('id');

            $form.find('.errorlist').remove();
            $.ajax({
                type: 'POST',
                url: $form.attr('action'),
                data: $form.serialize(),
                success: function (response) {
                    $form.find('.error-message').remove();
                    $('#messages').empty();
                    $('#messages').append(response.message_html);
                    $form.replaceWith(response.form_html);
                    bindAjaxForms();
                    hideSpinner();
                    initializeSpinnerAndButtons();
                    setTimeout(function () {
                        showAlertMessages(5000);
                    }, 100);
                },
                error: function (xhr, status, error) {
                    console.error(`Ошибка при отправке формы ${formId}:`, xhr.statusText, error);
                }
            });
        });
    }
});
