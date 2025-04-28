package com.smartstock.myapplication.recommendation


import android.view.View
import android.view.ViewGroup
import androidx.test.espresso.Espresso.onView
import androidx.test.espresso.UiController
import androidx.test.espresso.ViewAction
import androidx.test.espresso.action.ViewActions.*
import androidx.test.espresso.assertion.ViewAssertions.*
import androidx.test.espresso.matcher.ViewMatchers.*
import androidx.test.ext.junit.rules.ActivityScenarioRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.filters.LargeTest
import com.smartstock.myapplication.R
import com.smartstock.myapplication.SplashActivity
import com.smartstock.myapplication.Utils
import org.hamcrest.Description
import org.hamcrest.Matcher
import org.hamcrest.Matchers.allOf
import org.hamcrest.TypeSafeMatcher
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

@LargeTest
@RunWith(AndroidJUnit4::class)
class CreateRecommendationTest {

    @Rule
    @JvmField
    var mActivityScenarioRule = ActivityScenarioRule(SplashActivity::class.java)

    fun waitFor(millis: Long): ViewAction {
        return object : ViewAction {
            override fun getConstraints(): Matcher<View> = isRoot()

            override fun getDescription(): String = "Wait for $millis milliseconds."

            override fun perform(uiController: UiController, view: View?) {
                uiController.loopMainThreadForAtLeast(millis)
            }
        }
    }
    @Test
    fun createRecommendationTest() {
        onView(isRoot()).perform(waitFor(4000))
        val textInputEditText = onView(withId(R.id.email))
            .perform(replaceText("seller@seller.com"), closeSoftKeyboard())

        val textInputEditText2 = onView(withId(R.id.password))
            .perform(replaceText("123456"), closeSoftKeyboard())

        val materialButton = onView(withId(R.id.buttonLogin))
            .perform(click())

        onView(isRoot()).perform(waitFor(5000))
        val bottomNavigationItemView = onView(
            withId(R.id.nav_menu)
        )
        bottomNavigationItemView.perform(click())
        onView(isRoot()).perform(waitFor(1000))

        val materialTextView = onView(
            allOf(
                withId(android.R.id.title), withText(Utils.getLocalizedText("menu_cargar_video")),
                childAtPosition(
                    childAtPosition(
                        withId(android.R.id.content),
                        0
                    ),
                    0
                ),
                isDisplayed()
            )
        )
        materialTextView.perform(click())


        val materialAutoCompleteTextView = onView(
            allOf(
                withId(R.id.autoCompleteTextViewCreate1),
                childAtPosition(
                    childAtPosition(
                        withId(R.id.upload_vide_client),
                        0
                    ),
                    0
                ),
                isDisplayed()
            )
        )
        materialAutoCompleteTextView.perform(click())
        onView(isRoot()).perform(waitFor(200))



        /*val appCompatImageView = onView(
            allOf(
                withId(R.id.videoUploadIcon),
                childAtPosition(
                    allOf(
                        withId(R.id.section_upload_video_5),
                        childAtPosition(
                            withId(R.id.uploadvideo),
                            4
                        )
                    ),
                    0
                ),
                isDisplayed()
            )
        )
        appCompatImageView.perform(click())*/
        onView(withId(R.id.section_upload_video_5)).perform(click())
        onView(withId(R.id.uploadvideo)).perform(click())

        onView(isRoot()).perform(waitFor(10000))

        onView(withId(R.id.buttonAcceptCreate))
            .check(matches(isDisplayed()))
            .check(matches(isEnabled()))
            .perform(click())

        onView(isRoot()).perform(waitFor(2000))


        val textViewPPal = onView(withId(R.id.client_list))
        textViewPPal.check(matches(withText(Utils.getLocalizedText("lista_de_clientes"))))
    }

    private fun childAtPosition(
        parentMatcher: Matcher<View>, position: Int
    ): Matcher<View> {

        return object : TypeSafeMatcher<View>() {
            override fun describeTo(description: Description) {
                description.appendText("Child at position $position in parent ")
                parentMatcher.describeTo(description)
            }

            public override fun matchesSafely(view: View): Boolean {
                val parent = view.parent
                return parent is ViewGroup && parentMatcher.matches(parent)
                        && view == parent.getChildAt(position)
            }
        }
    }
}
