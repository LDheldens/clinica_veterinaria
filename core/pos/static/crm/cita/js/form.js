var fv;
var input_fecha;

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
            // Ajusta los campos y las validaciones según tu formulario de cita
            medico: {
                validators: {
                    notEmpty: {
                        message: 'El médico es obligatorio'
                    },
                }
            },
            asunto: {
                validators: {
                    notEmpty: {
                        message: 'El asunto es obligatorio'
                    },
                }
            },
            descripcion: {
                validators: {
                    notEmpty: {
                        message: 'La descripción es obligatoria'
                    },
                }
            },
            propietario: {
                validators: {
                    notEmpty: {
                        message: 'El propietario es obligatorio'
                    },
                }
            },
            fecha_cita: {
                validators: {
                    notEmpty: {
                        message: 'La fecha de la cita es obligatoria'
                    },
                }
            },
            hora_cita: {
                validators: {
                    notEmpty: {
                        message: 'La hora de la cita es obligatoria'
                    },
                }
            },
            mascota: {
                validators: {
                    notEmpty: {
                        message: 'La mascota es obligatoria'
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
    
    // Configuración del datepicker para el campo fecha_cita
    // input_fecha = $('input[name="fecha_cita"]');
    // input_fecha.datetimepicker({
    //     useCurrent: false,
    //     format: 'YYYY-MM-DD',
    //     locale: 'es',
    //     keepOpen: false,
    // });
    // input_fecha.datetimepicker('date', input_fecha.val());
    // input_fecha.on('change.datetimepicker', function (e) {
    //     fv.revalidateField('fecha_cita');
    // });
    
    // Validaciones adicionales para campos de texto
    $('input[name="mascota"]').keypress(function (e) {
        return validate_form_text('letters', e, null);
    });
    $('input[name="medicinas_aplicadas"]').keypress(function (e) {
        return validate_form_text('letters', e, null);
    });
    $('input[name="motivo"]').keypress(function (e) {
        return validate_form_text('letters', e, null);
    });
    $('input[name="antecedentes"]').keypress(function (e) {
        return validate_form_text('letters', e, null);
    });
    $('input[name="tratamiento"]').keypress(function (e) {
        return validate_form_text('letters', e, null);
    });
});
