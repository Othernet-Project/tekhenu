% rebase('base')

<section class="main">
    <div class="inner">
        <h1>{{ _('Broadcast administration') }}</h1>
        {{! h.form(_class='search') }}
            <p>
            {{! h.vinput('q', vals, _placeholder=_('Search'), _type="text") }}
            <button type="submit">{{ _('Go') }}</button>
            </p>
        </form>

        {{! h.form(_class='filters') }}
            <p>
            {{ _('show per page:') }}
            {{! h.vselect('pp', per_page, vals, _class="perpage") }}
            <button type="submit">{{ _('Reload') }}</button>
            <a class="button" href="{{ i18n_path(request.path) }}">Reset</a>
            </p>
        </form>

        <p class="controls">
        <a href="{{ i18n_path(h.set_qparam('select', 1)) }}">select all</a>
        <a href="{{ i18n_path(h.del_qparam('select')) }}">deselect all</a>
        </p>
        {{! h.form(method='post', csrf=True) }}
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
                        <th class="center">{{ _('repl.') }}</th>
                        <th class="center">{{ _('note') }}</th>
                        <th class="center"></th>
                    </tr>
                </thead>
                <tbody>
                    % if not content.count:
                        <tr>
                        <td class="center" colspan="9">{{ _('No content') }}</td>
                        </tr>
                    % else:
                        % for c in content.items:
                        <tr>
                            <td>{{! h.vcheckbox('selection', c.key.id(), vals, default=sel, _id=c.key.id()) }}</td>
                            <td><label class="plain" for="{{ c.key.id() }}">{{ c.title or c.url }}</label> <a class="external" href="{{ c.url }}" target="_blank">{{ _('open') }}</a></td>
                            <td class="center">{{ c.updated.strftime('%y-%m-%d %H:%M') }}</td>
                            <td class="center{{ c.is_controversial and ' controversial' or '' }}">{{ c.votes }}</td>
                            <td>{{ c.license_title }}</td>
                            <td class="center">{{ c.archive_title }}</td>
                            <td class="center">
                            % if c.replaces:
                            <span class="replaces">{{ c.replaces }}</span>
                            % else:
                            <span class="no-replaces"></span>
                            % end
                            </td>
                            <td class="center">
                            % if c.notes:
                            <span class+"note">{{ c.notes }}</span>
                            % else:
                            <span class="no-note"></span>
                            % end
                            </td>
                            <td class="center">
                            <a class="button-small" href="#">{{ _('details') }}</a>
                            </td>
                        </tr>
                        % end
                    % end
                </tbody>
            </table>

            % include('_pager', c=content)

            <h2>{{ _('Content actions') }}</h2>
            <p class="warn">
            {{ _('Please note that after performing any action, the list on this page may not update immediately. Wait a few seconds and refresh the page if the changes do not appear immediately') }}
            </p>
            <p class="archive">
            %# Translators, used as label for select box that sets archive for content
            {{! h.vselect('archive', Content.ARCHIVES, vals) }}
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
    <div class="inner filters">
        <h1>{{ _('Filters') }}</h2>
        {{! h.form(_class='filters') }} <p class="filters">
            {{! h.vselect('archives', Content.ARCHIVES, vals, empty=_('Archive')) }}
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
    </div>

    <div class="inner manual">
        <h1>{{ _('Manually add') }}</h1>
        {{! h.form(method='post', action=i18n_path(request.path + 'new/'), csrf=True) }}
            <p>
            <label for="url">{{ _('url:') }}*</label>
            {{! h.vinput('url', vals, _type="url", _placeholder=_('e.g., http://www.example.com/')) }}
            {{! h.field_error('url', errors) }}
            </p>
            <p>
            <label for="title">{{ _('page title:') }}</label>
            {{! h.vinput('title', vals, _type="text", _placeholder=_('e.g., Example page')) }}
            {{! h.field_error('title', errors) }}
            </p>
            <p>
            <label for="license">{{ _('license:') }}</label>
            {{! h.vselect('license', Content.LICENSES[1:], vals, empty=_('Unknown')) }}
            {{! h.field_error('license', errors) }}
            </p>
            <p>
            <label for="archive">{{ _('archive:') }}</label>
            {{! h.vselect('archive', Content.ARCHIVES, vals) }}
            {{! h.field_error('archive', errors) }}
            </p>
            <p class="buttons">
            <button type="submit">{{ _('Add') }}</button>
            </p>
        </form>
    </div>

    <div class="inner bulk">
        %# Translators, used as section above form for bulk-loading content information
        <h1>{{ _('Bulk load') }}</h2>
        {{! h.form(method='post', action=i18n_path(request.path + 'bulk/'), csrf=True) }}
            <p>
            <label for="data">{{ _('CSV data:') }}</label>
            <input name="data" id="data" type="file">
            {{! h.field_error('data', errors) }}
            </p>
            <p class="buttons">
            <button type="submit">{{ _('Upload') }}</button>
            </p>
        </form>
    </div>
</aside>
