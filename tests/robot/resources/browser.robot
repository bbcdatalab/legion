*** Settings ***
Documentation       Legion robot resources for browser tests
Library             Selenium2Library
Library             Collections

*** Variables ***
${BROWSER}                  Firefox
${SELENIUM_TIMEOUT}         60 seconds    #time to explicite wait for keywords run
${SELENIUM_IMPLICIT_WAIT}   5 seconds     #time to wait for a DOM load on page
${NEXUS_COMPONENTS_TABLE}   //table[contains(.,'docker')]
${NEXUS_HOST}               ${HOST_PROTOCOL}://nexus.${HOST_BASE_DOMAIN}

 #   LOCATORS
 ##  DEX AUTH PAGE
 ${DEX_AUTH_dex_email_login_button}   //button[contains(@class, 'dex-btn theme-btn-provider')]
 ${DEX_AUTH_login_input}              //*[@id="login"]
 ${DEX_AUTH_password_input}           //*[@id="password"]
 ${DEX_AUTH_login_button}             //*[@id="submit-login"]


*** Keywords ***
Start browser
    [Arguments]                  ${url}
    Open Browser                 ${url}                     ${BROWSER}
    Set Selenium Timeout         ${SELENIUM_TIMEOUT}
    Set Selenium Implicit Wait   ${SELENIUM_IMPLICIT_WAIT}
    Maximize Browser Window

Login with dex
     Wait Until Element Is Visible           xpath: ${DEX_AUTH_dex_email_login_button}
     Click Button                            xpath: ${DEX_AUTH_dex_email_login_button}
     Wait Until Element Is Visible           xpath: ${DEX_AUTH_login_input}
     Input Text 	                            xpath: ${DEX_AUTH_login_input} 	    ${STATIC_USER_EMAIL}
     Input Text 	                            xpath: ${DEX_AUTH_password_input} 	${STATIC_USER_PASS}
     Click Button                            xpath: ${DEX_AUTH_login_button}