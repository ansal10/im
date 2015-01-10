/**
 * Created by amd on 1/9/15.
 */
(function ($, window, UNDEFINED) {
    var sharingInitialized = false;

    function get_page_url(bEncode) {
        var url = document.location.href;
        return bEncode ? encodeURIComponent(url) : url;
    }

    function get_page_title(bEncode) {
        var title = $(document).find("title").text();
        return bEncode ? encodeURIComponent(title) : title;
    }

    function open_popup(url, name, width, height, scroll) {
        var left = ($(window).width() - width) / 2,
            top = ($(window).height() - height) / 2,
            opts = 'status=1,' + (scroll ? 'scrollbars=1,' : '') + 'width=' + width + ',height=' + height + ',top=' + top + ',left=' + left;

        window.open(url, name, opts);
    }

    function share_facebook() {
        open_popup("https://www.facebook.com/sharer/sharer.php?u=" + get_page_url(1), "", 600, 350);
    }

    function share_google_plus() {
        open_popup("https://plus.google.com/share?url=" + get_page_url(1), "", 500, 500);
    }

    function share_twitter() {
        open_popup("https://twitter.com/share?url=" + get_page_url(1) + "&text=" + get_page_title(1), "", 575, 400, true);
    }

    function share_linked_in() {
        open_popup("https://www.linkedin.com/shareArticle?mini=true&url=" + get_page_url(1) + "&title=" + get_page_title(1), "", 750, 400, true);
    }

    window.pb_init_sharing = function () {
        if (sharingInitialized) {
            return;
        }

        sharingInitialized = true;

        $('<div class="sharing-container hidden-xs"></div>')
            .appendTo(document.body)
            .append(
                $('<div class="sharing-item sharing-fb"><div class="sharing-img"></div></div>').click(share_facebook),
                $('<div class="sharing-item sharing-gp"><div class="sharing-img"></div></div>').click(share_google_plus),
                $('<div class="sharing-item sharing-tw"><div class="sharing-img"></div></div>').click(share_twitter),
                $('<div class="sharing-item sharing-li"><div class="sharing-img"></div></div>').click(share_linked_in)
            );
    };

})(jQuery, this);