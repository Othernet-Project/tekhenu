% rebase('base.tpl')

<secton>
    %# Translators, section title above content listing
    <h1>{{ _('Latest content') }}</h1>

    <form>
        <p class="search">
        {{! h.vinput('q', vals, _placeholder=_('Search')) }}
        <button type="submit">{{ _('Go') }}</button>
        </p>
        <p class="filters">
        {{! h.vselect('status', Content.STATI, vals, empty=_('Status')) }}
        {{! h.vselect('license', Content.LICENSES_SIMPLE, vals, empty=_('License')) }}
        {{! h.vselect('votes', Content.VOTES, vals, empty=_('Votes')) }}
        <button type="submit">{{ _('Filter') }}</button>
        </p>
    </form>

    % if not content.count:
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
            % for c in content.items:
            <tr>
                <td>
                %# Translators, appears next to URL in content list when there is no title
                <a href="{{ c.path }}">{{ h.yesno(c.title, c.title, '%s (%s)' % (c.url, _('no title'))) }}</a>
                </td>
                <td>
                {{ c.license_type }}
                </td>
                <td>
                {{ c.votes }}
                </td>
                <td>
                {{ c.status_title }}
                </td>
            </tr>
            % end
        </tbody>
    </table>
    % include('_pager', c=content)
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
        {{! h.vselect('license', Content.LICENSES, vals) }}
        {{! h.field_error('license', errors) }}
        <p>
        <p class="buttons">
        %# Translators, used as button label
        <button type="submit">{{ _('Suggest') }}</button>
        </p>
    </form>
</aside>

