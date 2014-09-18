% rebase('base')

<section>
    %# Translators, appears as page title on content details page if source page has not title
    <h1>{{ content.title or _('No title') }} <span>{{ content.status_title }}</span></h1>
    <p><a href="{{ content.url">{{ content.url }}</a></p>
    %# Translators, appears as label next to number of votes, should not be considered as a sentence
    <p>{{ content.votes }} <span>{{ ngettext('vote', 'votes', content.votes) }}</span></p>
    % if request.params.get('edit') == '1' and content.is_editable:
    <form method="POST">
        {{! csrf_token }}
        <p>
        %# Translators, used as label for content title
        <label for="title">{{ _('title:') }}</label>
        {{! h.vinput('title', vals) }}
        {{! h.field_error('title', errors) }}
        </p>
        <p>
        %# Translators, used as label for content title
        <label for="license">{{ _('license:') }}</label>
        {{! h.vselect('license', Content.LICENSES, vals) }}
        {{! h.field_error('license', errors) }}
        </p>
        <p class="buttons">
        <button type="submit">Save</button>
    </form>
    % else:
    <p>
    %# Translators, used as label for content title
    <span class="label">{{ _('title:') }}</span>
    {{ content.title or _('no title') }}
    % if content.is_editable:
        % include('_fix_button')
    % end
    </p>
    <p>
    %# Translators, used as label for content license
    <span class="label">{{ _('license:') }}</span>
    %# Translators, used instad of license name when license information is missing 
    {{ h.yesno(content.license, content.license_title, _('unknown')) }}
    % if content.is_editable:
        % include('_fix_button')
    % end
    </p>
    % end

    <h2>{{ _('Activity log') }}</h2>

    <ul>
    % for entry in content.log:
        <li>
        [{{ entry.timestamp }} UTC] {{ entry.title }} 
        %# Translators, used in entry log, %s is replaced with ip_address
        ({{ str(_('from %s')) % entry.ip_addr }})
        </li>
    % end
    </ul>
</section>

<aside>
% include('_suggestion_form')
</aside>
