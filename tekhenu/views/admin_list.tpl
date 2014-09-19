% rebase('base')

<section class="main">
    <div class="inner">
        <h1>{{ _('Broadcast administration') }}</h1>
        <form class="search">
            <p>
            {{! h.vinput('q', vals, _placeholder=_('Search'), _type="text") }}
            <button type="submit">{{ _('Go') }}</button>
            </p>
        </form>

        <form class="filters">
            <p>
            {{ _('show per page:') }}
            {{! h.vselect('pp', per_page, vals, _class="perpage") }}
            <button type="submit">{{ _('Reload') }}</button>
            </p>
        </form>

        <p class="controls">
        <a href="{{ i18n_path(h.set_qparam('select', 1)) }}">select all</a>
        <a href="{{ i18n_path(h.del_qparam('select')) }}">deselect all</a>
        </p>
        <form method="POST">
            {{! csrf_token }}
            % include('_pager', c=content)
            <table>
                <thead>
                    <tr>
                        <th></th>
                        <th>{{ _('title') }}</th>
                        <th class="center">{{ _('updated') }}</th>
                        <th class="center">{{ _('votes') }}</th>
                        <th>{{ _('license') }}</th>
                        <th class="center">{{ _('archive') }}</th>
                    </tr>
                </thead>
                <tbody>
                    % if not content.count:
                        <tr>
                        <td class="center" colspan="6">{{ _('No content') }}</td>
                        </tr>
                    % else:
                        % for c in content.items:
                        <tr>
                            <td>{{! h.vcheckbox('selection', c.key.id(), vals, default=sel, _id=c.key.id()) }}</td>
                            <td><label class="plain" for="{{ c.key.id() }}">{{ c.title or c.url }}</label> <a class="external" href="{{ c.url }}" target="_blank">{{ _('open') }}</a></td>
                            <td class="center">{{ c.updated.strftime('%y-%m-%d %H:%M') }}</td>
                            <td class="center">{{ c.votes }} (+{{c.upvotes}}/-{{c.downvotes}})</td>
                            <td>{{ c.license_title }}</td>
                            <td class="center">{{ c.archive_title }}</td>
                        </tr>
                        % end
                    % end
                </tbody>
            </table>

            % include('_pager', c=content)

            <h2>{{ _('Content actions') }}</h2>
            <p class="note">
            {{ _('Please note that after performing any action, the list on this pay may update immediately. Wait a few seconds and refresh the page if the changes do not appear immediately') }}
            </p>
            <p class="archive">
            %# Translators, used as label for select box that sets archive for content
            {{! h.vselect('archive', Content.ARCHIVES, vals, empty=_('Add to archive')) }}
            %# Translators, used as label for button that sets content options in broadcast list
            <button type="submit" name="action" value="status">{{ _('Update status') }}</button>
            </p>
            <p class="delete">
            %# Translators, used as label for button that deletes selected entities in broadcast list
            <button type="submit" name="action" value="delete">{{ _('Delete selected') }}</button>
            </p>
        </form>
    </div>
</section>

<aside class="sidebar">
    <div class="inner">
        <h1>{{ _('Filters') }}</h2>
        <form class="filters">
            <p class="filters">
            {{! h.vselect('archive', Content.ARCHIVES, vals, empty=_('Archive')) }}
            </p>
            <p>
            {{! h.vselect('license', licenses, vals, empty=_('License')) }}
            </p>
            <p>
            {{! h.vselect('votes', votes, vals, empty=_('Votes')) }}
            </p>
            <p>
            <button type="submit">{{ _('Filter') }}</button>
            <a class="button" href="{{ i18n_path(request.path) }}">Reset</a>
            </p>
        </form>

        %# Translators, used as section above form for bulk-loading content information
        <h1>{{ _('Bulk load') }}</h2>
        <p>TODO</p>
    </div>
</aside>
