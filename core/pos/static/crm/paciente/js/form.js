var current_date;

var select_client;

var fv;
var fvClient;

var fecha_nacimiento;
var input_birthdate;

document.addEventListener('DOMContentLoaded', function (e) {
    const frmClient = document.getElementById('frmClient');
    fvClient = FormValidation.formValidation(frmClient, {
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
                first_name: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                    }
                },
                last_name: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                    }
                },
                dni: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            // min: 8,
                            max: 8
                        },
                        digits: {},
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    obj: frmClient.querySelector('[name="dni"]').value,
                                    type: 'dni',
                                    action: 'validate_data'
                                };
                            },
                            message: 'El número de cedula ya se encuentra registrado',
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
                            min: 7
                        },
                        digits: {},
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    obj: frmClient.querySelector('[name="mobile"]').value,
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
                                    obj: frmClient.querySelector('[name="email"]').value,
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
                address: {
                    validators: {
                        stringLength: {
                            min: 4,
                        }
                    }
                },
                image: {
                    validators: {
                        file: {
                            extension: 'jpeg,jpg,png',
                            type: 'image/jpeg,image/png',
                            maxFiles: 1,
                            message: 'Introduce una imagen válida'
                        }
                    }
                },
                birthdate: {
                    validators: {
                        notEmpty: {
                            message: 'La fecha es obligatoria'
                        },
                        date: {
                            format: 'YYYY-MM-DD',
                            message: 'La fecha no es válida'
                        }
                    },
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
            const iconPlugin = fvClient.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(frmClient.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            var parameters = new FormData(fvClient.form);
            parameters.append('action', 'create_client');
            submit_formdata_with_ajax('Notificación', '¿Estas seguro de realizar la siguiente acción?', pathname,
                parameters,
                function (request) {
                    var newOption = new Option(request.user.full_name + ' / ' + request.user.dni, request.id, false, true);
                    console.log(newOption)
                    console.log(request.user.full_name + ' / ' + request.user.dni, request.id)
                    select_client.append(newOption).trigger('change');
                    fv.revalidateField('propietario');
                    $('#myModalClient').modal('hide');
                }
            );
        });
});

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
                fecha_nacimiento: {
                    validators: {
                        notEmpty: {
                            message: 'La fecha es obligatoria'
                        },
                        date: {
                            format: 'YYYY-MM-DD',
                            message: 'La fecha no es válida'
                        }
                    },
                },
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
                declaracion_jurada: {
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
    $('input[name="fecha_nacimiento"]').on('input', function() {
        // console.log('El valor del input ha cambiado a: ', $(this).val());
        const fechaNacimiento = new Date($(this).val());
        const hoy = new Date();
        let edad = hoy.getFullYear() - fechaNacimiento.getFullYear();
        // Verificar si el cumpleaños ya pasó este año
        if (hoy.getMonth() < fechaNacimiento.getMonth() || 
            (hoy.getMonth() === fechaNacimiento.getMonth() && hoy.getDate() < fechaNacimiento.getDate())) {
            edad--;
        }
        // console.log('Edad:', edad);
        $('input[name="edad"]').val(edad + ' año(s)')
    });

    select_client = $('select[name="propietario"]');
    current_date = new moment().format("YYYY-MM-DD");
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
    
    input_birthdate = $('input[name="birthdate"]');
    $('.btnAddClient').on('click', function () {
        input_birthdate.datetimepicker('date', new Date());
        $('#myModalClient').modal('show');
    });
    $('#myModalClient').on('hidden.bs.modal', function () {
        fvClient.resetForm(true);
    });
    input_birthdate.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
        maxDate: current_date
    });

    input_birthdate.on('change.datetimepicker', function (e) {
        fvClient.revalidateField('birthdate');
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