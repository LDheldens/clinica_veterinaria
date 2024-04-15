var fv;

document.addEventListener('DOMContentLoaded', function (e) {
    const form = document.getElementById('frmForm'); // Reemplaza 'frmForm' con el ID de tu formulario
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
            paciente: {
                validators: {
                    notEmpty: {
                        message: 'El paciente es obligatorio'
                    }
                }
            },
            // fecha_diagnostico: {
            //     validators: {
            //         notEmpty: {
            //             message: 'La fecha del diagnóstico es obligatoria'
            //         }
            //     }
            // },
            medico: {
                validators: {
                    notEmpty: {
                        message: 'El médico veterinario es obligatorio'
                    }
                }
            },
            sintomas: {
                validators: {
                    notEmpty: {
                        message: 'Los síntomas son obligatorios'
                    }
                }
            },
            examenes_fisicos: {
                validators: {
                    notEmpty: {
                        message: 'Este campo es obligatorio'
                    }
                }
            },
            observacion_veterinario: {
                validators: {
                    notEmpty: {
                        message: 'La observación del veterinario es obligatoria'
                    }
                }
            },
            diagnostico_provicional: {
                validators: {
                    notEmpty: {
                        message: 'El diagnóstico provicional es obligatorio'
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
    
    // Eventos para limitar entrada de texto
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

