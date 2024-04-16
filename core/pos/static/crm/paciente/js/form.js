var fv;
var fecha_nacimiento;

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
                identificacion: {
                    validators: {
                        notEmpty: {
                            message: 'La identificación es obligatoria'
                        },
                        regexp: {
                            regexp: /^SVT-\d+$/,
                            message: 'La identificación no coincide con el formato (SVT-1)'
                        },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    obj: form.querySelector('[name="identificacion"]').value,
                                    type: 'identificacion',
                                    action: 'validate_data'
                                };
                            },
                            message: 'La identificacion ya se encuentra registrado',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                        }
                    },
                },
                propietario: {
                    validators: {
                        notEmpty: {
                            message: 'El propietario es obligatorio'
                        },
                    }
                },
                nombre: {
                    validators: {
                        stringLength: {
                            min: 2
                        },
                        notEmpty: {
                            message: 'El nombre de la mascota es obligatorio'
                        },
                    }
                },
                tipo_mascota: {
                    validators: {
                        notEmpty: {
                            message: 'El tipo de mascota es obligatorio'
                        },
                    }
                },
                sexo: {
                    validators: {
                        notEmpty: {
                            message: 'El sexo de la mascota es obligatorio'
                        },
                    }
                },
                tamanio: {
                    validators: {
                        notEmpty: {
                            message: 'El tamaño de la mascota es obligatorio'
                        },
                    }
                },
                // raza: {
                //     validators: {
                //         notEmpty: {
                //             message: 'La raza de la mascota es obligatorio'
                //         },
                //     }
                // },
                edad: {
                    validators: {
                        notEmpty: {
                            message: 'La edad de la mascota es obligatorio'
                        },
                    }
                },
                peso: {
                    validators: {
                        notEmpty: {
                            message: 'El peso de la mascota es obligatorio'
                        },
                    }
                },
            },
            
            // excluded: ':disabled'
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
    
    fecha_nacimiento = $('input[name="fecha_nacimiento"]');

    fecha_nacimiento.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
    });

    fecha_nacimiento.on('change.datetimepicker', function (e) {
        fv.revalidateField('fecha_nacimiento');
    });

    // $('input[name="identificacion"]').keypress(function (e) {
    //     return validate_form_text('letters_numbers_spaceless', e, null);
    // });
    $('input[name="nombre"]').keypress(function (e) {
        return validate_form_text('letters', e, null);
    });
    $('input[name="tamanio"]').keypress(function (e) {
        return validate_form_text('decimals', e, null);
    });
    $('input[name="edad"]').keypress(function (e) {
        return validate_form_text('numbers', e, null);
    });
    $('input[name="peso"]').keypress(function (e) {
        return validate_form_text('decimals', e, null);
    });
    // $('input[name="descripcion"]').keypress(function (e) {
    //     return validate_form_text('letters', e, null);
    // });
});