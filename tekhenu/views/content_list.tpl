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
% include('_suggestion_form')
<aside>
