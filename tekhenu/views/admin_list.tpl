% rebase('base')

<h1>{{ _('Content') }}</h1>

<form>
    <p class="search">
    {{! h.vinput('q', vals, _placeholder=_('Search')) }}
    <button type="submit">{{ _('Go') }}</button>
    </p>
    <p class="filters">
    {{! h.vselect('archive', Content.ARCHIVES, vals, empty=_('Archive')) }}
    {{! h.vselect('license', licenses, vals, empty=_('License')) }}
    {{! h.vselect('votes', votes, vals, empty=_('Votes')) }}
    <button type="submit">{{ _('Filter') }}</button>
    {{ _('show per page:') }}
    {{! h.vselect('pp', per_page, vals) }}
    <button type="submit">{{ _('Reload') }}</button>
    </p>
</form>

<form method="POST">
    {{! csrf_token }}
    <p class="controls">
    <a href="{{ i18n_path(h.set_qparam('select', '1')) }}">select all</a>
    <a href="{{ i18n_path(h.del_qparam('select')) }}">deselect all</a>
    </p>
    % include('_pager', c=content)
    <table>
        <thead>
            <tr>
                <th></th>
                <th>{{ _('title') }}</th>
                <th>{{ _('link') }}</th>
                <th>{{ _('votes') }}</th>
                <th>{{ _('ratio') }}</th>
                <th>{{ _('license') }}</th>
                <th>{{ _('archive') }}</th>
            </tr>
        </thead>
        <tbody>
            % if not content.count:
                <tr>
                <td colspan="6">{{ _('No content') }}</td>
                </tr>
            % else:
                % for c in content.items:
                <tr>
                    <td>{{! h.vcheckbox('selection', c.key.id(), vals, default=sel) }}</td>
                    <td>{{ c.title or c.url }}</td>
                    <td><a href="{{ c.url }}" target="_blank">{{ _('open') }}</a></td>
                    <td>{{ c.votes }} (+{{c.upvotes}}/-{{c.downvotes}})</td>
                    <td>{{ c.votes_ratio }}</td>
                    <td>{{ c.license_title }}</td>
                    <td>{{ c.archive_title }}</td>
                </tr>
                % end
            % end
        </tbody>
    </table>
    % include('_pager', c=content)
    <div class="controls">
    %# Translators, used as label for select box that sets archive for content
    {{! h.vselect('archive', Content.ARCHIVES, vals, empty=_('Add to archive')) }}
    %# Translators, used as label for button that sets content options in broadcast list
    <button type="submit" name="action" value="set">{{ _('Set') }}</button>
    %# Translators, used as label for button that deletes selected entities in broadcast list
    <button type="submit" name="action" value="delete">{{ _('Delete selected') }}</button>
    </div>
</form>
