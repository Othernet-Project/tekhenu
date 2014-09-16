% rebase('base.tpl')

<secton>
    %# Translators, section title above content listing
    <h1>{{ _('Latest content') }}</h1>

    % if not content:
    <p>No content</p>
    % else:
    <table>
        <thead>
            <tr>
                <th>title</th>
                <th>license</th>
                <th>votes</th>
                <th>status</th>
            </tr>
        </thead>
        <tbody>
            % for c in content:
            <tr>
                <td>
                <a href="{{ c.path }}">{{ c.title }}</a>
                </td>
                <td>
                {{ c.license_type }}
                </td>
                <td>
                {{ c.votes }}
                </td>
                <td>
                {{ h.yesno(c.on_air, h.yesno(c.is_core, _('core'), _('on air')), _('off air')) }}
                </td>
            </tr>
            % end
        </tbody>
    </table>
    % end
</section>

<aside>
    %# Translators, section title above suggestion form
    <h1>{{ _('Suggest content') }}</h1>

    <p>
    %# Translators, shown above suggestion form
    {{! _('Here you can suggest content that shuould be broadcast over <a href="https://www.outernet.is/">Outernet</a>.') }}
    </p>

    <form method="POST" class="suggestion">
        {{! csrf_token }}
        <p class="url">
        <label for="url">{{ _('Page address (URL):') }}</label>
        %# Translators, used as form field label in suggestion form
        {{! h.vinput('url', vals, _type='url', placeholder=_('e.g., http://www.example.com/')) }}
        {{! h.field_error('url', errors) }}
        </p>
        <p class="license">
        %# Translators, used as form field label in suggestion form
        <label for="url">{{ _('Content license:') }}</label>
        {{! h.vselect('license', licenses, vals) }}
        {{! h.field_error('license', errors) }}
        <p>
        <p class="buttons">
        %# Translators, used as button label
        <button type="submit">{{ _('Suggest') }}</button>
        </p>
    </form>
</aside>

