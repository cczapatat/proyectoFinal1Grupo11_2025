package com.smartstock.myapplication.seller


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
import org.hamcrest.Description
import org.hamcrest.Matcher
import org.hamcrest.Matchers.allOf
import org.hamcrest.TypeSafeMatcher
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

@LargeTest
@RunWith(AndroidJUnit4::class)
class ListSellerClientsTest {

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
    fun listSellerClientsTest() {
        onView(isRoot()).perform(waitFor(4000))

        val textInputEditText = onView(withId(R.id.email))
            .perform(replaceText("seller1@sta.com"), closeSoftKeyboard())

        val textInputEditText2 = onView(withId(R.id.password))
            .perform(replaceText("1234567"), closeSoftKeyboard())

        val materialButton = onView(withId(R.id.buttonLogin))
            .perform(click())

        onView(isRoot()).perform(waitFor(4000))
        onView(isRoot()).perform(waitFor(10000))

        val cardView = onView(allOf(
            withId(R.id.cardViewClient),
            isDescendantOfA(withId(R.id.clientsRv)),  // Assuming it's inside a RecyclerView
            hasDescendant(withText("client1"))          // Match a unique child view
        ))

         cardView.check(matches(isDisplayed()))
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
