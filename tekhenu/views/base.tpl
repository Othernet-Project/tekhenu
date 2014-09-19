<!doctype html>

<html>
    <head>
        <meta chraset="utf8">
        <meta http-equiv="Content-Type" content="text/html; charset=utf8">
        <link rel="shortcut icon" href="/favicon.ico">
        {{! meta }}
        <link rel="stylesheet" href="/static/css/{{ css }}.css">
    </head>
    <body>
        <header class="header">
            <p class="logo">
            {{! h.link_other('<img src="/static/img/logo.png" alt="Tekhenu via Outernet">', i18n_path('/'), i18n_path(request.path)) }}
            </p>
            <p class="sponsor">
            <a class="button-large" href="/not-implemented">{{ _('Sponsor your favorite content') }}</a>
            </p>
            % if len(languages) > 1:
                <nav class="languages">
                % for locale, lang in languages:
                    % if locale != request.locale:
                    <a href="{{ i18n_path(locale=locale) }}">{{ lang }}</a>
                    % else:
                    <span class="current">{{ lang }}</span>
                    % end
                % end
                </nav>
            % end
        </header>

        % if message != '':
        <aside class="message">
        <a class="close" href="{{ i18n_path(request.path) }}">close</a>
        <p class="message-text"><strong>{{ message }}</strong></p>
        </aside>
        % end

        <div class="content">
        {{! base }}
        </div>

        <footer class="footer">
            <p class="bottom-logo">
            <a href="https://www.outernet.is/">{{ _("OUTERNET: Humanity's public library") }}</a>
            </p>
        </footer>
    </body>
</html>
