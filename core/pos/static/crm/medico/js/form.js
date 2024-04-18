var fv;

document.addEventListener('DOMContentLoaded', function (e) {
    const form = document.getElementById('frmForm'); // Reemplaza 'id_medico_form' con el ID de tu formulario
    fv = FormValidation.formValidation(form, {
        locale: 'es_ES',
        localization: FormValidation.locales.es_ES,
        plugins: {
            trigger: new FormValidation.plugins.Trigger(),
            submitButton: new FormValidation.plugins.SubmitButton(),
            bootstrap: new FormValidation.plugins.Bootstrap(),
            icon: new FormValidation.plugins.Icon({
                valid: 'fa fa-check',
                invalid: 'fa fa-times',
                validating: 'fa fa-refresh',
            }),
        },
        fields: {
            certificado: {
                validators: {
                    validators: {
                        file: {
                            extension: 'pdf',
                            type: 'application/pdf',
                            maxFiles: 1,
                            message: 'Introduce un archivo de pdf válido'
                        }
                    }
                }
            },
            especialidad: {
                validators: {
                    notEmpty: {
                        message: 'La especialidad es obligatoria'
                    }
                }
            },
            first_name: {
                validators: {
                    notEmpty: {
                        message: 'El nombre es obligatorio'
                    }
                }
            },
            last_name: {
                validators: {
                    notEmpty: {
                        message: 'El apellido es obligatorio'
                    }
                }
            },
            codigo_medico: {
                validators: {
                    notEmpty: {
                        message: 'El código del médico es obligatorio'
                    },
                    digits: {},
                    remote: {
                        url: pathname,
                        data: function () {
                            return {
                                obj: form.querySelector('[name="codigo_medico"]').value,
                                type: 'codigo_medico',
                                action: 'validate_data'
                            };
                        },
                        message: 'Este Código ya se encuentra registrado',
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': csrftoken
                        },
                    }
                }
            },
            dni: {
                validators: {
                    notEmpty: {},
                    stringLength: {
                        max:8
                    },
                    digits: {},
                    remote: {
                        url: pathname,
                        data: function () {
                            return {
                                obj: form.querySelector('[name="dni"]').value,
                                type: 'dni',
                                action: 'validate_data'
                            };
                        },
                        message: 'El número de DNI ya se encuentra registrado',
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': csrftoken
                        },
                    }
                }
            },
            mobile: {
                validators: {
                    notEmpty: {},
                    stringLength: {
                        min: 9,
                        max: 9, // Asegura que acepte solo 9 dígitos
                        message: 'El número de teléfono debe contener exactamente 9 dígitos'
                    },
                    digits: {},
                    remote: {
                        url: pathname,
                        data: function () {
                            return {
                                obj: form.querySelector('[name="mobile"]').value,
                                type: 'mobile',
                                action: 'validate_data'
                            };
                        },
                        message: 'El número de teléfono ya se encuentra registrado',
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': csrftoken
                        },
                    }
                }
            },
            email: {
                validators: {
                    notEmpty: {},
                    stringLength: {
                        min: 5
                    },
                    regexp: {
                        regexp: /^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/i,
                        message: 'El formato email no es correcto'
                    },
                    remote: {
                        url: pathname,
                        data: function () {
                            return {
                                obj: form.querySelector('[name="email"]').value,
                                type: 'email',
                                action: 'validate_data'
                            };
                        },
                        message: 'El email ya se encuentra registrado',
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': csrftoken
                        },
                    }
                }
            },
        }
    })
    .on('core.element.validated', function (e) {
        if (e.valid) {
            const groupEle = FormValidation.utils.closest(e.element, '.form-group');
            if (groupEle) {
                FormValidation.utils.classSet(groupEle, {
                    'has-success': false,
                });
            }
            FormValidation.utils.classSet(e.element, {
                'is-valid': false,
            });
        }
        const iconPlugin = fv.getPlugin('icon');
        const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
        iconElement && (iconElement.style.display = 'none');
    })
    .on('core.validator.validated', function (e) {
        if (!e.result.valid) {
            const messages = [].slice.call(form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
            messages.forEach((messageEle) => {
                const validator = messageEle.getAttribute('data-validator');
                messageEle.style.display = validator === e.validator ? 'block' : 'none';
            });
        }
    })
    .on('core.form.valid', function () {
        submit_formdata_with_ajax_form(fv);
    });

    $('input[name="dni"]').keypress(function (e) {
        return validate_form_text('numbers', e, null);
    });
    $('input[name="first_name"]').keypress(function (e) {
        return validate_form_text('letters', e, null);
    });
    $('input[name="last_name"]').keypress(function (e) {
        return validate_form_text('letters', e, null);
    });
    $('input[name="mobile"]').keypress(function (e) {
        return validate_form_text('numbers', e, null);
    });
});
