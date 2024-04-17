var fv;

document.addEventListener('DOMContentLoaded', function (e) {
    const form = document.getElementById('frmForm');
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
            // Ajusta los campos y las validaciones según tu formulario de cirugía
            paciente: {
                validators: {
                    notEmpty: {
                        message: 'El nombre del cachorro es obligatorio'
                    },
                }
            },
            medico: {
                validators: {
                    notEmpty: {
                        message: 'El nombre del médico es obligatorio'
                    },
                }
            },
            cliente: {
                validators: {
                    notEmpty: {
                        message: 'El nombre del cliente es obligatorio'
                    },
                }
            },
            fecha: {
                validators: {
                    notEmpty: {
                        message: 'La fecha es obligatoria'
                    },
                }
            },
            hora: {
                validators: {
                    notEmpty: {
                        message: 'La hora es obligatoria'
                    },
                }
            },
            firma_propietario: {
                validators: {
                    notEmpty: {
                        message: 'La firma del propietario es obligatoria'
                    },
                }
            },
        },
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
});

$(function () {
    // Validaciones adicionales para campos de texto
    $('input[name="cachorro"]').keypress(function (e) {
        return validate_form_text('letters', e, null);
    });
    $('input[name="medico"]').keypress(function (e) {
        return validate_form_text('letters', e, null);
    });
    $('input[name="cliente"]').keypress(function (e) {
        return validate_form_text('letters', e, null);
    });
});
