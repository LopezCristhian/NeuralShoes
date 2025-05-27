<#import "template.ftl" as layout>
<@layout.registrationLayout displayInfo=true displayMessage=!messagesPerField.existsError('username'); section>
    <#if section = "header">
        ¿Olvidaste tu contraseña?
    <#elseif section = "form">
        <form id="kc-reset-password-form" class="${properties.kcFormClass!}" action="${url.loginAction}" method="post">
            <div class="${properties.kcFormGroupClass!}">
                <div class="${properties.kcLabelWrapperClass!}">
                    <label for="username" class="${properties.kcLabelClass!}">
                        <#if !realm.loginWithEmailAllowed>
                            Nombre de usuario
                        <#elseif !realm.registrationEmailAsUsername>
                            Usuario o correo electrónico
                        <#else>
                            Correo electrónico
                        </#if>
                    </label>
                </div>
                <div class="${properties.kcInputWrapperClass!}">
                    <input type="text" id="username" name="username" class="${properties.kcInputClass!}" autofocus value="${(auth.attemptedUsername!'')}" aria-invalid="<#if messagesPerField.existsError('username')>true</#if>" dir="ltr"/>
                    <#if messagesPerField.existsError('username')>
                        <span id="input-error-username" class="${properties.kcInputErrorMessageClass!}" aria-live="polite">
                            ${kcSanitize(messagesPerField.get('username'))?no_esc}
                        </span>
                    </#if>
                </div>
            </div>
            <div class="${properties.kcFormGroupClass!} ${properties.kcFormSettingClass!}">
                <div id="kc-form-options" class="${properties.kcFormOptionsClass!}">
                    <div class="${properties.kcFormOptionsWrapperClass!}">
                        <span><a href="${url.loginUrl}">Volver al inicio de sesión</a></span>
                    </div>
                </div>

                <div id="kc-form-buttons" class="${properties.kcFormButtonsClass!}">
                    <input class="${properties.kcButtonClass!} ${properties.kcButtonPrimaryClass!} ${properties.kcButtonBlockClass!} ${properties.kcButtonLargeClass!}" type="submit" value="Enviar enlace de recuperación"/>
                </div>
            </div>
        </form>
    <#elseif section = "info" >
        <#if realm.duplicateEmailsAllowed>
            Ingresa tu nombre de usuario y te enviaremos instrucciones para restablecer tu contraseña.
        <#else>
            Ingresa tu correo electrónico y te enviaremos instrucciones para restablecer tu contraseña.
        </#if>
    </#if>
</@layout.registrationLayout>