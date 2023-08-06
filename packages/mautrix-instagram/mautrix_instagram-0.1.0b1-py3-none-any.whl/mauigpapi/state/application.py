# mautrix-instagram - A Matrix-Instagram puppeting bridge.
# Copyright (C) 2020 Tulir Asokan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import pkgutil
import json

from attr import dataclass

from mautrix.types import SerializableAttrs

default_capabilities = json.loads(pkgutil.get_data("mauigpapi.state",
                                                   "samples/supported-capabilities.json"))


@dataclass
class AndroidApplication(SerializableAttrs['AndroidApplication']):
    # TODO these newer versions make the iris subscribe stop working for some reason
    # APP_VERSION: str = "168.0.0.40.355"
    # APP_VERSION_CODE: str = "261079771"
    # APP_VERSION: str = "167.1.0.25.120"
    # APP_VERSION_CODE: str = "259829117"
    APP_VERSION: str = "159.0.0.29.122"
    APP_VERSION_CODE: str = "244390482"
    BREADCRUMB_KEY: str = "iN4$aGr0m"
    FACEBOOK_ANALYTICS_APPLICATION_ID: str = "567067343352427"
    FACEBOOK_OTA_FIELDS: str = (
        "update%7Bdownload_uri%2Cdownload_uri_delta_base%2Cversion_code_delta_base"
        "%2Cdownload_uri_delta%2Cfallback_to_full_update%2Cfile_size_delta%2Cversion_code"
        "%2Cpublished_date%2Cfile_size%2Cota_bundle_type%2Cresources_checksum"
        "%2Cresources_sha256_checksum%2Callowed_networks%2Crelease_id%7D "
    )
    FACEBOOK_ORCA_APPLICATION_ID: str = "124024574287414"

    BLOKS_VERSION_ID: str = "0e00f30ed0184b9c914a8baad3fe538aa36a9f0faad173486e76af5ee9310d0b"
    CAPABILITIES: str = "3brTvx8="
    SUPPORTED_CAPABILITIES: str = default_capabilities

    EXPERIMENTS: str = ",".join((
        "ig_android_ad_stories_scroll_perf_universe", "ig_android_ads_bottom_sheet_report_flow",
        "ig_android_ads_data_preferences_universe", "ig_android_ads_rendering_logging",
        "ig_android_canvas_cookie_universe", "ig_android_feed_ads_ppr_universe",
        "ig_android_graphql_survey_new_proxy_universe", "ig_android_viewpoint_occlusion",
        "ig_android_viewpoint_stories_public_testing",
        "ig_promote_interactive_poll_sticker_igid_universe", "ig_stories_ads_delivery_rules",
        "ig_stories_ads_media_based_insertion", "ig_android_li_session_chaining",
        "ig_android_logging_metric_universe_v2", "mi_viewpoint_viewability_universe",
        "ig_android_branded_content_appeal_states",
        "ig_android_branded_content_tag_redesign_organic",
        "ig_branded_content_settings_unsaved_changes_dialog",
        "ig_branded_content_tagging_approval_request_flow_brand_side_v2",
        "ig_rn_branded_content_settings_approval_on_select_save",
        "aymt_instagram_promote_flow_abandonment_ig_universe",
        "ig_android_account_insights_shopping_content_universe",
        "ig_android_business_attribute_sync", "ig_android_business_promote_tooltip",
        "ig_android_business_transaction_in_stories_consumer",
        "ig_android_business_transaction_in_stories_creator",
        "ig_android_create_page_on_top_universe", "ig_android_fb_sync_options_universe",
        "ig_android_fb_url_universe", "ig_android_fbpage_on_profile_side_tray",
        "ig_android_insights_post_dismiss_button", "ig_android_location_integrity_universe",
        "ig_android_personal_user_xposting_destination_fix", "ig_android_place_signature_universe",
        "ig_android_product_breakdown_post_insights", "ig_android_secondary_inbox_universe",
        "ig_android_share_publish_page_universe",
        "ig_android_skip_button_content_on_connect_fb_universe",
        "ig_business_new_value_prop_universe", "ig_android_business_cross_post_with_biz_id_infra",
        "ig_android_claim_location_page", "ig_android_edit_location_page_info",
        "ig_android_page_claim_deeplink_qe", "ig_biz_growth_insights_universe",
        "android_cameracore_fbaudio_integration_ig_universe",
        "android_ig_cameracore_aspect_ratio_fix", "ig_android_arengine_remote_scripting_universe",
        "ig_android_camera_formats_ranking_universe", "ig_android_camera_gyro_universe",
        "ig_android_camera_reduce_file_exif_reads",
        "ig_android_enable_automated_instruction_text_ar",
        "ig_android_image_exif_metadata_ar_effect_id_universe", "ig_android_optic_face_detection",
        "ig_android_optic_new_architecture", "ig_android_optic_photo_cropping_fixes",
        "ig_android_recognition_tracking_thread_prority_universe", "ig_android_ttcp_improvements",
        "ig_camera_android_bg_processor",
        "ig_camera_android_effect_metadata_cache_refresh_universe",
        "ig_camera_android_facetracker_v12_universe",
        "ig_camera_android_feed_effect_attribution_universe",
        "ig_camera_android_gallery_search_universe",
        "ig_camera_android_gyro_senser_sampling_period_universe",
        "ig_camera_android_paris_filter_universe", "ig_camera_android_share_effect_link_universe",
        "ig_camera_android_subtle_filter_universe", "ig_cameracore_android_new_optic_camera2",
        "ig_cameracore_android_new_optic_camera2_galaxy",
        "ig_android_external_gallery_import_affordance",
        "ig_android_feed_auto_share_to_facebook_dialog", "ig_android_fs_creation_flow_tweaks",
        "ig_android_fs_new_gallery", "ig_android_fs_new_gallery_hashtag_prompts",
        "ig_android_music_story_fb_crosspost_universe", "ig_android_partial_share_sheet",
        "ig_android_photo_creation_large_width", "ig_android_render_thread_memory_leak_holdout",
        "ig_android_direct_add_member_dialog_universe",
        "ig_android_direct_aggregated_media_and_reshares",
        "ig_android_direct_block_from_group_message_requests",
        "ig_android_direct_inbox_cache_universe",
        "ig_android_direct_leave_from_group_message_requests",
        "ig_android_direct_mark_as_read_notif_action", "ig_android_direct_message_follow_button",
        "ig_android_direct_multi_upload_universe", "ig_android_direct_mutation_manager_media_3",
        "ig_android_direct_new_gallery", "ig_android_direct_segmented_video",
        "ig_android_direct_state_observer", "ig_android_direct_thread_target_queue_universe",
        "ig_android_direct_view_more_qe",
        "ig_android_direct_wellbeing_message_reachability_settings",
        "ig_android_disable_manual_retries", "ig_android_gallery_grid_controller_folder_cache",
        "ig_android_multi_thread_sends", "ig_android_on_notification_cleared_async_universe",
        "ig_android_push_reliability_universe",
        "ig_android_wait_for_app_initialization_on_push_action_universe",
        "ig_direct_android_bubble_system", "ig_direct_max_participants",
        "ig_android_explore_recyclerview_universe", "ig_android_explore_reel_loading_state",
        "ig_android_not_interested_secondary_options",
        "ig_android_save_to_collections_bottom_sheet_refactor",
        "ig_android_save_to_collections_flow", "ig_android_smplt_universe",
        "ig_explore_2018_post_chaining_account_recs_dedupe_universe",
        "ig_explore_2019_h1_destination_cover", "ig_explore_2019_h1_video_autoplay_resume",
        "ig_explore_reel_ring_universe", "ig_android_feed_cache_update",
        "ig_android_view_info_universe", "ig_carousel_bumped_organic_impression_client_universe",
        "ig_end_of_feed_universe", "ig_android_igtv_autoplay_on_prepare",
        "ig_android_igtv_browse_long_press", "ig_android_igtv_explore2x2_viewer",
        "ig_android_igtv_pip", "ig_android_igtv_player_follow_button",
        "ig_android_igtv_refresh_tv_guide_interval", "ig_android_igtv_stories_preview",
        "ig_android_igtv_whitelisted_for_web", "ig_android_biz_story_to_fb_page_improvement",
        "ig_android_contact_point_upload_rate_limit_killswitch",
        "ig_android_country_code_fix_universe", "ig_android_dual_destination_quality_improvement",
        "ig_android_explore_discover_people_entry_point_universe",
        "ig_android_fb_follow_server_linkage_universe", "ig_android_fb_link_ui_polish_universe",
        "ig_android_fb_profile_integration_universe", "ig_android_fbc_upsell_on_dp_first_load",
        "ig_android_ig_personal_account_to_fb_page_linkage_backfill",
        "ig_android_inline_editing_local_prefill", "ig_android_interest_follows_universe",
        "ig_android_invite_list_button_redesign_universe",
        "ig_android_login_onetap_upsell_universe", "ig_android_new_follower_removal_universe",
        "ig_android_persistent_nux", "ig_android_qp_kill_switch",
        "ig_android_recommend_accounts_destination_routing_fix",
        "ig_android_self_following_v2_universe", "ig_android_self_story_button_non_fbc_accounts",
        "ig_android_self_story_setting_option_in_menu",
        "ig_android_separate_empty_feed_su_universe",
        "ig_android_show_create_content_pages_universe",
        "ig_android_show_self_followers_after_becoming_private_universe",
        "ig_android_suggested_users_background",
        "ig_android_test_not_signing_address_book_unlink_endpoint",
        "ig_android_test_remove_button_main_cta_self_followers_universe",
        "ig_android_unfollow_from_main_feed_v2", "ig_android_unfollow_reciprocal_universe",
        "ig_android_unify_graph_management_actions",
        "ig_android_whats_app_contact_invite_universe",
        "ig_android_xposting_feed_to_stories_reshares_universe",
        "ig_android_xposting_newly_fbc_people", "ig_android_xposting_reel_memory_share_universe",
        "ig_android_zero_rating_carrier_signal", "ig_fb_graph_differentiation",
        "ig_graph_evolution_holdout_universe", "ig_graph_management_h2_2019_universe",
        "ig_graph_management_production_h2_2019_holdout_universe", "ig_inventory_connections",
        "ig_pacing_overriding_universe", "ig_sim_api_analytics_reporting",
        "ig_xposting_biz_feed_to_story_reshare", "ig_xposting_mention_reshare_stories",
        "instagram_ns_qp_prefetch_universe", "ig_android_analytics_background_uploader_schedule",
        "ig_android_appstate_logger", "ig_android_apr_lazy_build_request_infra",
        "ig_android_camera_leak", "ig_android_crash_fix_detach_from_gl_context",
        "ig_android_dead_code_detection", "ig_android_disk_usage_logging_universe",
        "ig_android_dropframe_manager", "ig_android_image_upload_quality_universe",
        "ig_android_mainfeed_generate_prefetch_background", "ig_android_media_remodel",
        "ig_android_memory_use_logging_universe", "ig_android_network_perf_qpl_ppr",
        "ig_android_qpl_class_marker", "ig_android_react_native_email_sms_settings_universe",
        "ig_android_sharedpreferences_qpl_logging", "ig_disable_fsync_universe",
        "ig_mprotect_code_universe", "ig_prefetch_scheduler_backtest",
        "ig_traffic_routing_universe", "ig_android_qr_code_nametag", "ig_android_qr_code_scanner",
        "ig_android_live_egl10_compat", "ig_android_live_realtime_comments_universe",
        "ig_android_live_subscribe_user_level_universe", "ig_android_tango_cpu_overuse_universe",
        "igqe_pending_tagged_posts", "ig_android_enable_zero_rating",
        "ig_android_sso_kototoro_app_universe", "ig_android_sso_use_trustedapp_universe",
        "ig_android_whitehat_options_universe",
        "ig_android_payments_growth_promote_payments_in_payments",
        "ig_android_purx_native_checkout_universe",
        "ig_android_shopping_pdp_post_purchase_sharing", "ig_payment_checkout_cvv",
        "ig_payment_checkout_info", "ig_payments_billing_address",
        "ig_android_profile_thumbnail_impression", "ig_android_user_url_deeplink_fbpage_endpoint",
        "instagram_android_profile_follow_cta_context_feed",
        "ig_android_mqtt_cookie_auth_memcache_universe", "ig_android_realtime_mqtt_logging",
        "ig_rti_inapp_notifications_universe", "ig_android_live_webrtc_livewith_params",
        "saved_collections_cache_universe", "ig_android_search_nearby_places_universe",
        "ig_search_hashtag_content_advisory_remove_snooze",
        "ig_android_shopping_bag_null_state_v1", "ig_android_shopping_bag_optimization_universe",
        "ig_android_shopping_checkout_signaling",
        "ig_android_shopping_product_metadata_on_product_tiles_universe",
        "ig_android_wishlist_reconsideration_universe", "ig_biz_post_approval_nux_universe",
        "ig_commerce_platform_ptx_bloks_universe", "ig_shopping_bag_universe",
        "ig_shopping_checkout_improvements_universe",
        "ig_shopping_checkout_improvements_v2_universe", "ig_shopping_checkout_mvp_experiment",
        "ig_shopping_insights_wc_copy_update_android", "ig_shopping_size_selector_redesign",
        "instagram_shopping_hero_carousel_visual_variant_consolidation",
        "ig_android_audience_control", "ig_android_camera_upsell_dialog",
        "ig_android_create_mode_memories_see_all", "ig_android_create_mode_tap_to_cycle",
        "ig_android_create_mode_templates", "ig_android_feed_post_sticker",
        "ig_android_frx_creation_question_responses_reporting",
        "ig_android_frx_highlight_cover_reporting_qe", "ig_android_music_browser_redesign",
        "ig_android_publisher_stories_migration", "ig_android_rainbow_hashtags",
        "ig_android_recipient_picker", "ig_android_reel_tray_item_impression_logging_viewpoint",
        "ig_android_save_all", "ig_android_stories_blacklist",
        "ig_android_stories_boomerang_v2_universe", "ig_android_stories_context_sheets_universe",
        "ig_android_stories_gallery_sticker_universe",
        "ig_android_stories_gallery_video_segmentation", "ig_android_stories_layout_universe",
        "ig_android_stories_music_awareness_universe", "ig_android_stories_music_lyrics",
        "ig_android_stories_music_overlay", "ig_android_stories_music_search_typeahead",
        "ig_android_stories_project_eclipse", "ig_android_stories_question_sticker_music_format",
        "ig_android_stories_quick_react_gif_universe",
        "ig_android_stories_share_extension_video_segmentation",
        "ig_android_stories_sundial_creation_universe", "ig_android_stories_video_prefetch_kb",
        "ig_android_stories_vpvd_container_module_fix", "ig_android_stories_weblink_creation",
        "ig_android_story_bottom_sheet_clips_single_audio_mas",
        "ig_android_story_bottom_sheet_music_mas", "ig_android_story_bottom_sheet_top_clips_mas",
        "ig_android_xposting_dual_destination_shortcut_fix",
        "ig_stories_allow_camera_actions_while_recording", "ig_stories_rainbow_ring",
        "ig_threads_clear_notifications_on_has_seen", "ig_threads_sanity_check_thread_viewkeys",
        "ig_android_action_sheet_migration_universe", "ig_android_emoji_util_universe_3",
        "ig_android_recyclerview_binder_group_enabled_universe",
        "ig_emoji_render_counter_logging_universe", "ig_android_delete_ssim_compare_img_soon",
        "ig_android_reel_raven_video_segmented_upload_universe",
        "ig_android_render_output_surface_timeout_universe",
        "ig_android_sidecar_segmented_streaming_universe",
        "ig_android_stories_video_seeking_audio_bug_fix", "ig_android_video_abr_universe",
        "ig_android_video_call_finish_universe", "ig_android_video_exoplayer_2",
        "ig_android_video_fit_scale_type_igtv", "ig_android_video_product_specific_abr",
        "ig_android_video_qp_logger_universe", "ig_android_video_raven_bitrate_ladder_universe",
        "ig_android_video_raven_passthrough", "ig_android_video_raven_streaming_upload_universe",
        "ig_android_video_streaming_upload_universe",
        "ig_android_video_upload_hevc_encoding_universe", "ig_android_video_upload_quality_qe1",
        "ig_android_video_upload_transform_matrix_fix_universe",
        "ig_android_video_visual_quality_score_based_abr",
        "ig_video_experimental_encoding_consumption_universe",
        "ig_android_vc_background_call_toast_universe", "ig_android_vc_capture_universe",
        "ig_android_vc_codec_settings", "ig_android_vc_cowatch_config_universe",
        "ig_android_vc_cowatch_media_share_universe", "ig_android_vc_cowatch_universe",
        "ig_android_vc_cpu_overuse_universe", "ig_android_vc_explicit_intent_for_notification",
        "ig_android_vc_face_effects_universe", "ig_android_vc_join_timeout_universe",
        "ig_android_vc_migrate_to_bluetooth_v2_universe",
        "ig_android_vc_missed_call_call_back_action_universe",
        "ig_android_vc_shareable_moments_universe",
        "ig_android_comment_warning_non_english_universe", "ig_android_feed_post_warning_universe",
        "ig_android_image_pdq_calculation", "ig_android_logged_in_delta_migration",
        "ig_android_wellbeing_support_frx_cowatch_reporting",
        "ig_android_wellbeing_support_frx_hashtags_reporting",
        "ig_android_wellbeing_timeinapp_v1_universe", "ig_challenge_general_v2",
        "ig_ei_option_setting_universe"
    ))
    LOGIN_EXPERIMENTS: str = "".join((
        "ig_android_device_detection_info_upload", "ig_android_device_info_foreground_reporting",
        "ig_android_suma_landing_page", "ig_android_device_based_country_verification",
        "ig_android_direct_add_direct_to_android_native_photo_share_sheet",
        "ig_android_direct_main_tab_universe_v2",
        "ig_account_identity_logged_out_signals_global_holdout_universe",
        "ig_android_fb_account_linking_sampling_freq_universe",
        "ig_android_login_identifier_fuzzy_match", "ig_android_nux_add_email_device",
        "ig_android_passwordless_account_password_creation_universe",
        "ig_android_reg_modularization_universe", "ig_android_retry_create_account_universe",
        "ig_growth_android_profile_pic_prefill_with_fb_pic_2",
        "ig_android_quickcapture_keep_screen_on", "ig_android_gmail_oauth_in_reg",
        "ig_android_reg_nux_headers_cleanup_universe", "ig_android_smartlock_hints_universe",
        "ig_android_security_intent_switchoff", "ig_android_sim_info_upload",
        "ig_android_caption_typeahead_fix_on_o_universe",
        "ig_android_video_render_codec_low_memory_gc", "ig_android_device_verification_fb_signup",
        "ig_android_device_verification_separate_endpoint"
    ))
