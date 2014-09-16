<!doctype html>

<html>
    <head>
        <meta chraset="utf8">
        <meta http-equiv="Content-Type" content="text/html; charset=utf8">
        {{! meta }}
    </head>
    <body>
        <header class="footer">
            <p class="logo">
            Tekhenu <a href="https://www.outernet.is/">{{ _('via Outernet') }}</a>
            </p>
            <p class="sponsor">
            <a href="/not-implemented">{{ _('Sponsor your favorite content') }}</a>
            </p>
            <nav class="languages">
            % for locale, lang in languages:
                % if locale != request.locale:
                <a href="{{ i18n_path(locale=locale) }}">{{ lang }}</a>
                % else:
                <span class="current">{{ lang }}</span>
                % end
            % end
            </nav>
        </header>

        <aside class="message">
        <p class="message-text"><strong>{{ message }}</strong></p>
        </aside>

        {{! base }}

        <footer class="footer">
            <p class="bottom-logo">
            {{ _("OUTERNET: Humanity's public library") }}
            </p>
        </footer>
    </body>
</html>
