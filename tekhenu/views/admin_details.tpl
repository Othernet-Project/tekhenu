% rebase('base', css='admin')

<section class="main content-details">
    <div class="inner">
        %# Translators, appears as page title on content details page if source page has not title
        <h1>{{ content.title or _('No title') }} <span class="status-{{ content.status }}">{{ content.status_title }}</span></h1>
        <p class="url"><a class="external" href="{{ content.url }}" target="_blank">{{ h.trunc(content.url, 40) }}</a></p>

        <p class="votes">
        <span class="count">{{ content.votes }}</span> 
        <span class="label">{{ ngettext('vote', 'votes', content.votes) }}</span>
        </p>

        % if request.params.get('edit') == '1':
            % if not content.is_editable:
            <p class="warn">
            {{ _('Note that editing the details for this content could make the metadata out of sync with content currently being broadcast.') }}
            </p>
            % end
            <form class="content-edit" method="POST">
                {{! csrf_token }}
                <p>
                %# Translators, used as label for content title
                <label for="title">{{ _('title:') }}</label>
                {{! h.vinput('title', vals, _type="text") }}
                {{! h.field_error('title', errors) }}
                </p>
                <p>
                %# Translators, used as label for content title
                <label for="license">{{ _('license:') }}</label>
                {{! h.vselect('license', Content.LICENSES, vals) }}
                {{! h.field_error('license', errors) }}
                </p>
                <p>
                %# Translators, used as label for an ID the content replaces
                <label for="replaces">{{ _('replaces:') }}</label>
                {{! h.vinput('replaces', vals, _type="text") }}
                {{! h.field_error('replaces', errors) }}
                </p>
                <p>
                %# Translators, used as label for partner/sponsor name
                <label for="partner">{{ _('source:') }}</label>
                {{! h.vinput('partner', vals, _type="text") }}
                {{! h.field_error('partner', errors) }}
                </p>
                <p>
                %# Translators, used as label for partner content flag checkbox
                <label for="is_partner">{{ _('partner:') }}</label>
                {{! h.vcheckbox('flags', 'is_partner', vals, _id='is_partner') }}
                {{! h.field_error('is_partner', errors) }}
                </p>
                <p class="buttons">
                <button type="submit">Save</button>
                </p>
            </form>
        % else:
            <p>
            %# Translators, used as label for content title
            <span class="label">{{ _('title:') }}</span>
            {{ content.title or _('no title') }}
            </p>
            <p>
            %# Translators, used as label for content license
            <span class="label">{{ _('license:') }}</span>
            %# Translators, used instad of license name when license information is missing 
            {{ h.yesno(content.license, content.license_title, _('unknown')) }}
            </p>
            <p>
            %# Translators, used as label for an ID the content replaces
            <span class="label">{{ _('replaces:') }}</span>
            {{ content.replaces or _('None') }}
            </p>
            <p>
            %# Translators, used as label for partner/sponsor name
            <span class="label">{{ _('source:') }}</span>
            {{ content.partner or _('None') }}
            </p>
            <p>
            %# Translators, used as label for partner content flag
            <span class="label">{{ _('partner:') }}</span>
            {{ h.yesno(content.is_partner, _('Yes'), _('No')) }}
            </p>

            <p>
            %# Translators, used as button label in broadcast admin on content details page
            <a class="button" href="{{ i18n_path(h.set_qparam('edit', 1)) }}">{{ _('Edit details') }}</a>
            </p>
        % end

        <h2>{{ _('Non-editable information') }}</h2>

        <p>
        %# Translators, used as label for sponsored content flag checkbox
        <span class="label">{{ _('sponsored:') }}</span>
        {{ h.yesno(content.is_sponsored, _('Yes'), _('No')) }}
        </p>

        <p>
        %# Translators, used as label for archive
        <span class="label">{{ _('archive:') }}</span>
        {{ content.archive_title }}
        </p>

        <h2>{{ _('Votes') }}</h2>
        <p>
        %# Translators, used as label for upvotes
        <span class="label">{{ _('upvotes:') }}</span>
        {{ content.upvotes }}
        </p>
        <p>
        %# Translators, used as label for downvotes
        <span class="label">{{ _('downvotes:') }}</span>
        {{ content.downvotes }}
        </p>
        <p>
        %# Translators, used as label for overall vote balance
        <span class="label">{{ _('overall:') }}</span>
        {{ content.votes }}
        </p>
        <p>
        %# Translators, used as label for vote balance factor
        <span class="label">{{ _('balance:') }}</span>
        {{ content.votes_ratio }} : 1
        </p>

        <h2>{{ _('Notes') }}</h2>

        {{! h.form(method='post', action=i18n_path(content.admin_path) + '/notes', csrf=True) }}
            <textarea name="notes">{{ content.notes or '' }}</textarea>
            <p class="buttons">
                <button type="submit">{{ _('Save') }}</button>
            </p>
        </form>

        <h2>{{ _('Activity log') }}</h2>

        <p>{{ str(ngettext('Showing %s event.', 'Showing %s events.', len(content.log))) % len(content.log) }}</p>

        <ul class="log">
        % for entry in content.log:
            <li>
            <span class="timestamp">[{{ entry.timestamp }} UTC - {{ entry.ip_addr }}]</span>
            <span class="entry">{{ entry.title }}</span>
            </li>
        % end
        </ul>
    </div>
</section>

<aside class="sidebar">
    <div class="inner">
        
    </div>
</aside>
