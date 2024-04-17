var fv;
var fecha_ingreso;
var fecha_salida;

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
                mascota: {
                    validators: {
                        notEmpty: {
                            message: 'El tipo de mascota es obligatorio'
                        },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    obj: form.querySelector('[name="mascota"]').value,
                                    type: 'mascota',
                                    action: 'validate_data'
                                };
                            },
                            message: 'Este paciente ya esta internado',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                        }
                    }
                },
                medicinas_aplicadas: {
                    validators: {
                        notEmpty: {
                            message: 'Las medicinas aplicadas son obligatorias'
                        },
                        stringLength: {
                            min: 2
                        },
                    }
                },
                motivo: {
                    validators: {
                        notEmpty: {
                            message: 'El motivo es obligatorio'
                        },
                        stringLength: {
                            min: 2
                        },
                    }
                },
                antecedentes: {
                    validators: {
                        notEmpty: {
                            message: 'Los antecedentes son obligatorios'
                        },
                        stringLength: {
                            min: 2
                        },
                    }
                },
                tratamiento: {
                    validators: {
                        notEmpty: {
                            message: 'El tratamiento es obligatorio'
                        },
                        stringLength: {
                            min: 2
                        },
                    }
                },
            },
        }
    )
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
    
    
    fecha_ingreso = $('input[name="fecha_ingreso"]');
    fecha_salida = $('input[name="fecha_salida"]');
    console.log({
        fecha_ingreso,
        fecha_salida
    })

    fecha_ingreso.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
    });
    fecha_salida.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
    });
    fecha_ingreso.on('change.datetimepicker', function (e) {
        fv.revalidateField('fecha_ingreso');
    });
    fecha_salida.on('change.datetimepicker', function (e) {
        fv.revalidateField('fecha_salida');
    });

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