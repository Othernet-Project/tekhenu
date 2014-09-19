% rebase('base')

<section class="main content-details">
    <div class="inner">
        %# Translators, appears as page title on content details page if source page has not title
        <h1>{{ content.title or _('No title') }} <span class="status-{{ content.status }}">{{ content.status_title }}</span></h1>
        <p class="url"><a class="external" href="{{ content.url }}" target="_blank">{{ h.trunc(content.url, 40) }}</a></p>

        % if content.is_editable:
        <form action="{{ i18n_path(content.path + '/votes/') }}" method="POST">
        {{! csrf_token }}
        {{! h.HIDDEN('back', request.path) }}
        <p class="votes">
        <button class="vote-up" name="vote" value="up">{{ _('vote up') }}</button>
        <span class="count">{{ content.votes }}</span> 
        <button class="vote-down" name="vote" value="down">{{ _('vote down') }}</button>
        %# Translators, appears as label next to number of votes, should not be considered as a sentence
        <span class="label">{{ ngettext('vote', 'votes', content.votes) }}</span>
        </p>
        </form>
        % else:
        <p class="votes">
        <span class="count">{{ content.votes }}</span> 
        <span class="label">{{ ngettext('vote', 'votes', content.votes) }}</span>
        </p>
        % end

        % if request.params.get('edit') == '1' and content.is_editable:
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

        <h2>{{ _('Activity log') }}</h2>

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

<aside class="suggestion-form">
    <div class="inner">
        % include('_suggestion_form')
    </div>
</aside>
